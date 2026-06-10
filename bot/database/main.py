import logging
from contextlib import asynccontextmanager
from sqlalchemy import event

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from bot.database.dsn import dsn
from bot.misc import SingletonMeta


class Database(metaclass=SingletonMeta):
    BASE = declarative_base()

    def __init__(self):
        db_url = dsn()
        self._is_sqlite = db_url.startswith("sqlite")

        engine_kwargs = {
            "echo": False,
        }

        if self._is_sqlite:
            # SQLite এর জন্য সেটিংস
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        else:
            # PostgreSQL এর জন্য সেটিংস
            engine_kwargs["pool_pre_ping"] = True
            engine_kwargs["pool_size"] = 20
            engine_kwargs["max_overflow"] = 40
            engine_kwargs["pool_timeout"] = 30
            engine_kwargs["pool_recycle"] = 3600
            engine_kwargs["connect_args"] = {
                "timeout": 10,
                "command_timeout": 30,
                "server_settings": {
                    "lc_messages": "C",
                },
            }

        self.__engine: AsyncEngine = create_async_engine(db_url, **engine_kwargs)

        # SQLite এ ফরেন কী সক্রিয় করুন
        if self._is_sqlite:
            @event.listens_for(self.__engine.sync_engine, "connect")
            def _set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.close()

            logging.info("ডাটাবেস শুরু হয়েছে: SQLite (WAL মোড)")
        else:
            logging.info("ডাটাবেস পুল শুরু হয়েছে: size=20, max_overflow=40")

        self.__SessionLocal = async_sessionmaker(
            bind=self.__engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self):
        """অ্যাসিঙ্ক কনটেক্সচুয়াল সেশন: ত্রুটিতে ক্লোজ/রোলব্যাক নিশ্চিত।"""
        async with self.__SessionLocal() as db:
            try:
                yield db
                await db.commit()
            except Exception:
                await db.rollback()
                raise

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine

    async def dispose(self):
        """কানেকশন পুল বন্ধ করুন।"""
        await self.__engine.dispose()