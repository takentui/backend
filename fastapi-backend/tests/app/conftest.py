from typing import AsyncGenerator

import pytest
from app import registry as db_registry
from sqlalchemy.sql import text

TRUNCATE_QUERY = "TRUNCATE TABLE {tbl_name} CASCADE;"


@pytest.fixture
async def clear_db() -> AsyncGenerator[None, None]:
    yield
    async with db_registry.engine.begin() as conn:
        await conn.execute(
            text(TRUNCATE_QUERY.format(tbl_name=app.db.customer_info.Customer.__tablename__))
        )
