from typing import Any

from app.api.deps import RedisDep, SessionDep, is_superuser
from app.core.redis import delete_cache, get_cache, set_cache
from app.crud.categories import create_category, get_all_categories
from app.models.categories import CategoriesPub, Category, CategoryCreate
from fastapi import APIRouter

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get(
    "",
    response_model=CategoriesPub,
)
async def categories(session: SessionDep, redis_client: RedisDep) -> Any:
    """Get all categories."""
    cache_key = "categories:all"

    # Try to get from cache first
    cached_data = await get_cache(redis_client, cache_key)
    if cached_data is not None:
        return CategoriesPub(**cached_data)

    # Cache miss - fetch from database
    categories_data = get_all_categories(session=session)

    # Store in cache for future requests
    await set_cache(redis_client, cache_key, categories_data.model_dump())

    return categories_data


@categories_router.post(
    "",
    response_model=Category,
    dependencies=[is_superuser],
)
async def new_category(session: SessionDep, redis_client: RedisDep, category: CategoryCreate) -> Any:
    """Create a new category."""
    # Create the new category
    new_category = create_category(session=session, category=category)

    # Invalidate the cache to ensure fresh data on next request
    cache_key = "categories:all"
    await delete_cache(redis_client, cache_key)

    return new_category
