from typing import Any

from app.api.deps import RedisDep, SessionDep, is_superuser
from app.core.cache_decorators import cache_get, cache_invalidate
from app.crud.categories import create_category, get_all_categories
from app.models.categories import CategoriesPub, Category, CategoryCreate
from fastapi import APIRouter

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get(
    "",
    response_model=CategoriesPub,
)
@cache_get("categories:all")
async def categories(session: SessionDep, redis_client: RedisDep) -> Any:
    """Get all categories."""
    return get_all_categories(session=session)


@categories_router.post(
    "",
    response_model=Category,
    dependencies=[is_superuser],
)
@cache_invalidate("categories:all")
async def new_category(session: SessionDep, redis_client: RedisDep, category: CategoryCreate) -> Any:
    """Create a new category."""
    return create_category(session=session, category=category)
