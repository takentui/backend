from typing import AsyncGenerator, Generator

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from app import database as db_config
from app import registry


@pytest.fixture(autouse=True)
async def _registry() -> AsyncGenerator[None, None]:
    await registry.setup()
    yield
    await registry.close()


@pytest.fixture(autouse=True, scope="session")
def migrate_db() -> Generator[None, None, None]:
    if db_config.dsn.host not in ("postgres", "localhost"):
        raise RuntimeError("Migration for tests should be applied only on test DB")

    config = AlembicConfig("alembic.ini")

    upgrade(config, "head")
    yield
    downgrade(config, "base")
