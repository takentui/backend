from typing import Any, Callable

from app import config
from app.config.db import DBConfig
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool


class DBRegistry:
    _config: DBConfig
    engine: AsyncEngine
    session: Callable[..., Session]
    base: Any

    def __init__(self, cfg: DBConfig):
        self._config = cfg
        self.base = declarative_base()

    async def setup(self) -> None:
        self.engine = create_async_engine(
            self._config.dsn.raw_dsn,
            connect_args={"server_settings": self._config.dsn.server_settings},
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self._config.pool_size,
            max_overflow=self._config.pool_max_overflow,
            pool_recycle=self._config.pool_recycle,
            pool_timeout=self._config.pool_timeout,
        )
        self.session = sessionmaker(  # type: ignore
            self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def close(self) -> None:
        await self.engine.dispose()


registry = DBRegistry(config.database)
