from __future__ import annotations

import json
import logging
from typing import Any

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self) -> None:
        self._client: Redis | None = None

    async def connect(self, redis_url: str | None) -> None:
        if not redis_url:
            return
        try:
            self._client = Redis.from_url(redis_url, decode_responses=True)
            await self._client.ping()
        except Exception as exc:  # pragma: no cover - Redis is optional locally.
            logger.warning("Redis cache disabled: %s", exc)
            self._client = None

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def get_json(self, key: str) -> Any | None:
        if self._client is None:
            return None
        raw = await self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: Any, ttl_seconds: int) -> None:
        if self._client is None:
            return
        await self._client.set(key, json.dumps(value, default=str), ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        if self._client is not None:
            await self._client.delete(key)


cache_service = CacheService()

