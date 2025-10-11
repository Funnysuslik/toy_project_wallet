import functools
from typing import Any, Callable, Optional

from app.core.redis import delete_cache, delete_cache_pattern, get_cache, set_cache


def cache_get(key: str):
    """
    Decorator for GET endpoints that implements caching.

    Args:
        key: Redis cache key to use for storing/retrieving data

    Usage:
        @cache_get("categories:all")
        async def get_categories(session: SessionDep, redis_client: RedisDep):
            return get_all_categories(session=session)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis_client = kwargs.get("redis_client")
            if not redis_client:
                return await func(*args, **kwargs)

            cached_data = await get_cache(redis_client, key)
            if cached_data is not None:
                from app.models.categories import CategoriesPub

                return CategoriesPub(**cached_data)

            result = await func(*args, **kwargs)

            if hasattr(result, "model_dump"):
                await set_cache(redis_client, key, result.model_dump())

            return result

        return wrapper

    return decorator


def cache_invalidate(*keys: str):
    """
    Decorator for POST/PUT/DELETE endpoints that invalidates cache.

    Args:
        keys: Redis cache keys to invalidate

    Usage:
        @cache_invalidate("categories:all")
        async def create_category(session: SessionDep, redis_client: RedisDep, category: CategoryCreate):
            return create_category(session=session, category=category)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            redis_client = kwargs.get("redis_client")
            if redis_client:
                for key in keys:
                    await delete_cache(redis_client, key)

            return result

        return wrapper

    return decorator


def cache_invalidate_pattern(*patterns: str):
    """
    Decorator for POST/PUT/DELETE endpoints that invalidates cache by pattern.

    Args:
        patterns: Redis cache key patterns to invalidate (supports wildcards)

    Usage:
        @cache_invalidate_pattern("categories:*", "wallets:*")
        async def bulk_update(session: SessionDep, redis_client: RedisDep):
            return bulk_update_operation(session=session)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            """Invalidate cache by pattern."""
            result = await func(*args, **kwargs)

            redis_client = kwargs.get("redis_client")
            if redis_client:
                for pattern in patterns:
                    await delete_cache_pattern(redis_client, pattern)

            return result

        return wrapper

    return decorator
