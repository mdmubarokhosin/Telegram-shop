import os
from pathlib import Path
from bot.misc import EnvKeys


def dsn() -> str:
    """ডাটাবেস URL ফেরত দিন। SQLite অথবা PostgreSQL সমর্থন করে।"""
    # যদি এনভায়রমেন্ট ভেরিয়েবল থাকে তাহলে সেটা ব্যবহার করুন
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url

    # ডকারে থাকলে DATABASE_URL ব্যবহার করুন
    if Path("/.dockerenv").exists():
        return EnvKeys.DATABASE_URL

    # DB_DRIVER অনুযায়ী সঠিক URL তৈরি করুন
    driver = EnvKeys.DB_DRIVER

    if "sqlite" in driver:
        db_path = os.getenv("SQLITE_DB_PATH", "data/shop.db")
        # ডাটাবেস ফোল্ডার তৈরি করুন
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+aiosqlite:///{db_path}"
    else:
        # PostgreSQL (ডিফল্ট)
        return EnvKeys.DATABASE_URL