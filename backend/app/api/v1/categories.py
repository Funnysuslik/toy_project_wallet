from typing import Any

from app.api.deps import SessionDep, is_superuser
from app.crud.categories import create_category, get_all_categories
from app.models.categories import CategoriesPub, Category, CategoryCreate
from fastapi import APIRouter

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get(
    "",
    response_model=CategoriesPub,
)
def categories(session: SessionDep) -> Any:

    return get_all_categories(session=session)


@categories_router.post(
    "",
    response_model=Category,
    dependencies=[is_superuser],
)
def new_category(session: SessionDep, category: CategoryCreate) -> Any:

    return create_category(session=session, category=category)
