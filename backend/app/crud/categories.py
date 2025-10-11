from app.models.categories import CategoriesPub, Category, CategoryCreate
from sqlmodel import Session, select


def get_all_categories(*, session: Session) -> CategoriesPub:
    """Get all categories."""
    q = select(Category)

    return CategoriesPub(data=session.exec(q).all())


def create_category(*, session: Session, category: CategoryCreate) -> Category:
    """Create a new category."""
    new_category = Category.model_validate(category)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category
