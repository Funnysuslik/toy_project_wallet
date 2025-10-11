import json
import logging
from collections.abc import Generator
from typing import Any, Optional

import redis.asyncio as redis
from app.core.settings import settings

logger = logging.getLogger(__name__)

# Global Redis connection pool
_redis_pool: Optional[redis.ConnectionPool] = None


def get_redis_pool() -> redis.ConnectionPool:
    """Get or create Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            db=settings.REDIS_DB,
            decode_responses=True,
            max_connections=20,
        )
    return _redis_pool


async def get_redis() -> Generator[redis.Redis, None, None]:
    """Get Redis client instance."""
    pool = get_redis_pool()
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.aclose()


async def get_cache(redis_client: redis.Redis, key: str) -> Optional[Any]:
    """Get cached data by key."""
    try:
        cached_data = await redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
    except Exception as e:
        logger.warning(f"Failed to get cache for key {key}: {e}")
        return None


async def set_cache(redis_client: redis.Redis, key: str, data: Any) -> bool:
    """Set cache data by key."""
    try:
        serialized_data = json.dumps(data, default=str)
        await redis_client.set(key, serialized_data)
        return True
    except Exception as e:
        logger.warning(f"Failed to set cache for key {key}: {e}")
        return False


async def delete_cache(redis_client: redis.Redis, key: str) -> bool:
    """Delete cache data by key."""
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Failed to delete cache for key {key}: {e}")
        return False


async def delete_cache_pattern(redis_client: redis.Redis, pattern: str) -> bool:
    """Delete cache data by pattern."""
    try:
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
        return True
    except Exception as e:
        logger.warning(f"Failed to delete cache for pattern {pattern}: {e}")
        return False
