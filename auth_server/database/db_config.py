import os
from typing import AsyncGenerator, Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import URL

load_dotenv()


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


PG_DB_NAME = get_env("PG_DB_NAME")
PG_DB_USER = get_env("PG_DB_USER")
PG_DB_PASSWD = get_env("PG_DB_PASSWD")
PG_DB_HOST = get_env("PG_DB_HOST")
PG_DB_PORT = get_env("PG_DB_PORT")
SQL_ECHO = get_env("SQL_ECHO").lower() == "true"

# Performance tuning variables
POOL_SIZE = int(get_env("DB_POOL_SIZE"))
MAX_OVERFLOW = int(get_env("DB_MAX_OVERFLOW"))
POOL_TIMEOUT = int(get_env("DB_POOL_TIMEOUT"))
POOL_RECYCLE = int(get_env("DB_POOL_RECYCLE"))

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=PG_DB_USER,
    password=PG_DB_PASSWD,
    host=PG_DB_HOST,
    port=int(PG_DB_PORT),
    database=PG_DB_NAME,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_pre_ping=True,
    pool_recycle=POOL_RECYCLE,
    pool_use_lifo=True,  # Use LIFO for better connection reuse
    connect_args={
        "server_settings": {
            "jit": "off",  # Disable JIT for faster query planning on simple queries
            "application_name": "auth_server_fastapi",
        },
        "command_timeout": 60,  # Query timeout in seconds
        "timeout": 30,  # Connection timeout
        "statement_cache_size": 0,  # Disable prepared statement cache for varied queries
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Auto-commit on success
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def check_db_health() -> bool:
    """Health check for database connectivity"""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False


async def close_db_engine() -> None:
    """Gracefully dispose database engine"""
    await engine.dispose()
