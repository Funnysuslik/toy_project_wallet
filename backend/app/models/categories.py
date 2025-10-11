from pydantic import field_validator
from pydantic_extra_types.color import Color
from sqlmodel import Field, Relationship, SQLModel


class TransactionsCategoriesLink(SQLModel, table=True):
    """Link table for transactions and categories."""

    transaction_id: int = Field(foreign_key="transaction.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)


class CategoryBase(SQLModel):
    """Base category model."""

    name: str = Field(max_length=100)
    color: str = Field(unique=True)


class CategoryCreate(CategoryBase):
    """Category creation model."""

    @field_validator("color", mode="before")
    def validate_and_convert_color(cls, v):
        if isinstance(v, Color):

            return v.as_hex()
        elif isinstance(v, str):
            try:
                c = Color(v)

                return c.as_hex()
            except Exception:
                raise ValueError("Invalid color string")
        raise ValueError("color must be a string or Color instance")


class CategoryPub(CategoryBase):
    """Category public model."""

    id: int


class CategoriesPub(SQLModel):
    """Categories public model."""

    data: list[CategoryPub]


class Category(CategoryBase, table=True):
    """Category model."""

    id: int | None = Field(default=None, primary_key=True)

    transactions: list["Transaction"] = Relationship(
        back_populates="categories",
        link_model=TransactionsCategoriesLink,
    )
