from typing import Any
from fastapi import APIRouter

from app.api.deps import SessionDep
from app.crud.categories import create_category, get_all_categories
from app.models.categories import Category, CategoryCreate, CategoriesPub


categories_router = APIRouter(prefix='/categories', tags=['Categories'])


@categories_router.get(
  '/',
  response_model=CategoriesPub,
)
def categories(session: SessionDep) -> Any:

  return get_all_categories(session)


@categories_router.post(
 '/' ,
 response_model=Category,
)
def new_category(session: SessionDep, category: CategoryCreate) -> Any:

  return create_category(session=session, category=category)
