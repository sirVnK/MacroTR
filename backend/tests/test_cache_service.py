from __future__ import annotations

import pytest

from app.services.cache_service import CacheService


@pytest.mark.asyncio
async def test_cache_service_noops_without_redis_client():
    cache = CacheService()

    assert await cache.get_json("missing") is None
    await cache.set_json("key", {"value": 1}, ttl_seconds=1)
    await cache.delete("key")

