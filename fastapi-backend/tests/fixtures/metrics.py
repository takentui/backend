from typing import AsyncGenerator

import prometheus_client
import pytest


@pytest.fixture
async def clean_metrics() -> AsyncGenerator:
    # pylint: disable=protected-access
    collectors = tuple(prometheus_client.REGISTRY._collector_to_names.keys())
    for collector in collectors:
        prometheus_client.REGISTRY.unregister(collector)
    yield
