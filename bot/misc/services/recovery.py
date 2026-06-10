import asyncio
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update, text

logger = logging.getLogger(__name__)


class RecoveryManager:
    """ডিজাস্টার রিকভারি ম্যানেজার — পেমেন্ট রিকভারি এবং হেলথ মনিটরিং"""

    def __init__(self, bot):
        self.bot = bot
        self.recovery_tasks = []
        self.running = False

    async def start(self):
        """রিকভারি সিস্টেম শুরু করা হচ্ছে"""
        logger.info("রিকভারি ম্যানেজার শুরু হচ্ছে...")
        self.running = True

        self.recovery_tasks.append(
            asyncio.create_task(self._safe_run(self.recover_pending_payments))
        )

        self.recovery_tasks.append(
            asyncio.create_task(self._safe_run(self.periodic_health_check))
        )

    async def stop(self):
        """রিকভারি সিস্টেম বন্ধ করা হচ্ছে"""
        self.running = False
        for task in self.recovery_tasks:
            task.cancel()
        await asyncio.gather(*self.recovery_tasks, return_exceptions=True)
        logger.info("রিকভারি ম্যানেজার বন্ধ হয়েছে")

    async def _safe_run(self, coro_func, *args):
        """নিরাপদ শুরু স্বয়ংক্রিয় পুনরায় আরম্ভ সহ ব্যর্থতার উপর"""
        while self.running:
            try:
                await coro_func(*args)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"রিকভারি টাস্ক ত্রুটি: {e}", exc_info=True)
                await asyncio.sleep(30)

    async def recover_pending_payments(self):
        """পেন্ডিং পেমেন্ট রিকভারি করা হচ্ছে — Bohudur পেমেন্ট চেক করা হবে"""
        from bot.database import Database
        from bot.database.models import Payments

        while self.running:
            try:
                payment_copies = []
                async with Database().session() as s:
                    cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
                    result = await s.execute(
                        select(Payments).where(
                            Payments.status == "pending",
                            Payments.created_at < cutoff,
                            Payments.provider == "bohudur"
                        )
                    )
                    pending_payments = result.scalars().all()

                    for p in pending_payments:
                        payment_copies.append({
                            'id': p.id,
                            'provider': p.provider,
                            'external_id': p.external_id,
                            'user_id': p.user_id,
                            'amount': p.amount,
                            'currency': p.currency,
                        })

                for pc in payment_copies:
                    await self._check_and_process_payment(pc)

            except Exception as e:
                logger.error(f"পেমেন্ট রিকভারি ত্রুটি: {e}")

            await asyncio.sleep(300)

    async def _check_and_process_payment(self, payment):
        """একটি নির্দিষ্ট পেমেন্ট যাচাই এবং প্রক্রিয়া করা"""
        from decimal import Decimal
        from bot.database.methods.transactions import process_payment_with_referral
        from bot.misc import EnvKeys
        from bot.misc.services.payment import BohudurAPI, BohudurAPIError
        from bot.i18n import localize

        p_id = payment['id'] if isinstance(payment, dict) else payment.id
        p_provider = payment['provider'] if isinstance(payment, dict) else payment.provider
        p_external_id = payment['external_id'] if isinstance(payment, dict) else payment.external_id
        p_user_id = payment['user_id'] if isinstance(payment, dict) else payment.user_id
        p_amount = payment['amount'] if isinstance(payment, dict) else payment.amount
        p_currency = payment['currency'] if isinstance(payment, dict) else payment.currency

        try:
            if p_provider == "bohudur" and EnvKeys.BOHUDUR_API_KEY:
                bohudur = BohudurAPI()
                info = await bohudur.query_payment(p_external_id)

                status = info.get("status", "")

                if status == "COMPLETED":
                    # পেমেন্ট সম্পন্ন হয়েছে — execute করুন
                    try:
                        await bohudur.execute_payment(p_external_id)
                    except BohudurAPIError:
                        pass  # ইতিমধ্যে execute হয়ে থাকতে পারে

                    balance_amount = int(info.get("amount", p_amount))

                    success, _ = await process_payment_with_referral(
                        user_id=p_user_id,
                        amount=Decimal(balance_amount),
                        provider=p_provider,
                        external_id=p_external_id,
                        referral_percent=EnvKeys.REFERRAL_PERCENT
                    )

                    if success:
                        logger.info(f"পেমেন্ট রিকভারি সফল: {p_external_id}")
                        try:
                            await self.bot.send_message(
                                p_user_id,
                                localize("payments.topped_simple", amount=balance_amount, currency=p_currency)
                            )
                        except Exception as e:
                            logger.error(f"ইউজারকে জানাতে ব্যর্থ {p_user_id}: {e}")

                elif status in ["CANCELLED", "EXPIRED", "FAILED"]:
                    await self._mark_payment_failed(p_id)

        except BohudurAPIError as e:
            logger.error(f"Bohudur API ত্রুটি পেমেন্ট {p_id}: [{e.code}] {e.message}")
        except Exception as e:
            logger.error(f"পেমেন্ট প্রক্রিয়াকরণ ত্রুটি {p_id}: {e}")

    async def _mark_payment_failed(self, payment_id: int):
        """পেমেন্ট ব্যর্থ হিসেবে চিহ্নিত করুন"""
        from bot.database import Database
        from bot.database.models import Payments

        async with Database().session() as s:
            await s.execute(
                update(Payments).where(Payments.id == payment_id).values(status="failed")
            )

    async def periodic_health_check(self):
        """নিয়মিত সিস্টেম হেলথ চেক"""
        from bot.database import Database

        while self.running:
            try:
                async with Database().session() as s:
                    await s.execute(text("SELECT 1"))

                from bot.misc.caching.cache import get_cache_manager
                cache = get_cache_manager()
                if cache:
                    await cache.check_health()
                    await cache.set("health:check", "ok", ttl=60)

                me = await self.bot.get_me()
                logger.debug(f"হেলথ চেক সফল: Bot @{me.username} সক্রিয় আছে")

            except Exception as e:
                logger.error(f"হেলথ চেক ব্যর্থ: {e}")

            await asyncio.sleep(60)