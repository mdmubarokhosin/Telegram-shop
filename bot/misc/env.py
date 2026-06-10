import logging
import os
from abc import ABC
from typing import Final
from urllib.parse import quote_plus

_env_logger = logging.getLogger(__name__)


class EnvKeys(ABC):
    """নিরাপদ এনভায়রমেন্ট কনফিগারেশন"""

    @staticmethod
    def _get_required(key: str) -> str:
        val = os.getenv(key)
        if not val:
            raise ValueError(f"প্রয়োজনীয় এনভায়রমেন্ট ভেরিয়েবল নেই: {key}")
        return val

    @staticmethod
    def _get_optional(key: str, default: str = "") -> str:
        return os.getenv(key, default)

    # === Telegram ===
    TOKEN: Final = _get_required('TOKEN')
    OWNER_ID: Final = int(_get_required('OWNER_ID'))

    # === ডাটাবেস ===
    # DB_DRIVER: "sqlite+aiosqlite" (Termux/লোকাল) অথবা "postgresql+asyncpg" (প্রোডাকশন)
    DB_DRIVER: Final = _get_optional("DB_DRIVER", "sqlite+aiosqlite")
    SQLITE_DB_PATH: Final = _get_optional("SQLITE_DB_PATH", "data/shop.db")

    # PostgreSQL (শুধুমাত্র প্রোডাকশনে প্রয়োজন)
    POSTGRES_DB: Final = _get_optional("POSTGRES_DB", "telegram_shop")
    POSTGRES_USER: Final = _get_optional("POSTGRES_USER", "shop_user")
    POSTGRES_PASSWORD: Final = _get_optional("POSTGRES_PASSWORD", "")
    DB_PORT: Final = int(_get_optional("DB_PORT", "5432"))
    POSTGRES_HOST: Final = _get_optional("POSTGRES_HOST", "localhost")

    # === Redis ===
    REDIS_ENABLED: Final = _get_optional("REDIS_ENABLED", "0")
    REDIS_HOST: Final = _get_optional("REDIS_HOST", "localhost")
    REDIS_PORT: Final = int(_get_optional("REDIS_PORT", "6379"))
    REDIS_DB: Final = int(_get_optional("REDIS_DB", "0"))
    REDIS_PASSWORD: Final = _get_optional("REDIS_PASSWORD", "")

    # === Bohudur পেমেন্ট ===
    BOHUDUR_API_KEY: Final = _get_required("BOHUDUR_API_KEY")
    BOHUDUR_WEBHOOK_URL: Final = _get_optional("BOHUDUR_WEBHOOK_URL", "")

    # === সাধারণ পেমেন্ট সেটিংস ===
    REFERRAL_PERCENT: Final = int(_get_optional("REFERRAL_PERCENT", "0"))
    PAY_CURRENCY: Final = _get_optional("PAY_CURRENCY", "BDT")
    PAYMENT_TIME: Final = int(_get_optional("PAYMENT_TIME", "1800"))
    MIN_AMOUNT: Final = int(_get_optional("MIN_AMOUNT", "10"))
    MAX_AMOUNT: Final = int(_get_optional("MAX_AMOUNT", "50000"))

    # === লিংক / UI ===
    CHANNEL_URL: Final = _get_optional("CHANNEL_URL", "")
    CHANNEL_ID: Final = _get_optional("CHANNEL_ID", "")
    HELPER_ID: Final = _get_optional("HELPER_ID", "")
    RULES: Final = _get_optional("RULES", "")

    # === ভাষা ও লগ ===
    BOT_LOCALE: Final = _get_optional("BOT_LOCALE", "bn")
    BOT_LOGFILE: Final = _get_optional("BOT_LOGFILE", "logs/bot.log")
    BOT_AUDITFILE: Final = _get_optional("BOT_AUDITFILE", "logs/audit.log")
    LOG_TO_STDOUT: Final = _get_optional("LOG_TO_STDOUT", "1")
    LOG_TO_FILE: Final = _get_optional("LOG_TO_FILE", "1")
    DEBUG: Final = _get_optional("DEBUG", "0")
    REVIEWS_ENABLED: Final = _get_optional("REVIEWS_ENABLED", "1")

    # === ওয়েব অ্যাডমিন প্যানেল ===
    ADMIN_HOST: Final = _get_optional("ADMIN_HOST", "localhost")
    ADMIN_PORT: Final = int(_get_optional("ADMIN_PORT", "9090"))
    ADMIN_USERNAME: Final = _get_optional("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: Final = _get_optional("ADMIN_PASSWORD", "admin")
    SECRET_KEY: Final = _get_optional("SECRET_KEY", "change-me-in-production")

    # === ওয়েবহুক ===
    WEBHOOK_ENABLED: Final = _get_optional("WEBHOOK_ENABLED", "0")
    WEBHOOK_URL: Final = _get_optional("WEBHOOK_URL", "")
    WEBHOOK_PATH: Final = _get_optional("WEBHOOK_PATH", "/webhook")
    WEBHOOK_SECRET: Final = _get_optional("WEBHOOK_SECRET", "")

    # === ক্লিনআপ ===
    AUDIT_RETENTION_DAYS: Final = int(_get_optional("AUDIT_RETENTION_DAYS", "90"))
    PAYMENTS_RETENTION_DAYS: Final = int(_get_optional("PAYMENTS_RETENTION_DAYS", "90"))

    # PostgreSQL URL (শুধুমাত্র PostgreSQL ব্যবহার করলে)
    DATABASE_URL: Final = f"postgresql+asyncpg://{POSTGRES_USER}:{quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:{DB_PORT}/{POSTGRES_DB}"

    # === স্টার্টআপ ভ্যালিডেশন ===
    if ADMIN_PASSWORD == "admin":
        _env_logger.warning(
            "নিরাপত্তা: ADMIN_PASSWORD ডিফল্ট মান 'admin' সেট করা আছে। "
            "এটি অবিলম্বে পরিবর্তন করুন।"
        )
    if SECRET_KEY == "change-me-in-production":
        _env_logger.warning(
            "নিরাপত্তা: SECRET_KEY ডিফল্ট মান সেট করা আছে। "
            "প্রোডাকশনে একটি শক্তিশালী SECRET_KEY সেট করুন।"
        )
    if int(MIN_AMOUNT) >= int(MAX_AMOUNT):
        _env_logger.warning(
            "কনফিগ: MIN_AMOUNT (%s) >= MAX_AMOUNT (%s)। "
            "পেমেন্ট পরিমাণ সবসময় বাতিল হবে।", MIN_AMOUNT, MAX_AMOUNT
        )
    if int(REFERRAL_PERCENT) < 0 or int(REFERRAL_PERCENT) > 99:
        _env_logger.warning(
            "কনফিগ: REFERRAL_PERCENT=%s বৈধ সীমার বাইরে [0, 99]।",
            REFERRAL_PERCENT,
        )