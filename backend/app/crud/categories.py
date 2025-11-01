from app.core.redis import delete_cache, get_cache, set_cache
from app.models.categories import CategoriesPub, Category, CategoryCreate
from sqlmodel import Session, select


async def get_all_categories(*, session: Session) -> CategoriesPub:
    """Get all categories."""
    cached_data = await get_cache(key="categories:all")
    if cached_data:
        return CategoriesPub(data=cached_data)

    categories = session.exec(select(Category)).all()
    await set_cache(key="categories:all", data=categories)
    return CategoriesPub(data=categories)


async def create_category(*, session: Session, category: CategoryCreate) -> Category:
    """Create a new category."""
    new_category = Category.model_validate(category)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    await delete_cache(key="categories:all")

    return new_category
