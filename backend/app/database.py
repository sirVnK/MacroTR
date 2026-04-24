from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()

engine = create_async_engine(
    settings.normalized_database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    from app.models import observation, series  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        if connection.dialect.name == "postgresql":
            await connection.execute(
                text(
                    """
                    ALTER TABLE series
                    ADD COLUMN IF NOT EXISTS last_successful_fetch TIMESTAMP WITH TIME ZONE,
                    ADD COLUMN IF NOT EXISTS last_fetch_attempt TIMESTAMP WITH TIME ZONE,
                    ADD COLUMN IF NOT EXISTS fetch_status VARCHAR(32) NOT NULL DEFAULT 'not_fetched',
                    ADD COLUMN IF NOT EXISTS fetch_error TEXT
                    """
                )
            )
