from pydantic_extra_types.color import Color
from pydantic import field_validator
from sqlmodel import Relationship, SQLModel, Field


class TransactionsCategoriesLink(SQLModel, table=True):
  transaction_id: int = Field(foreign_key='transaction.id', primary_key=True)
  category_id: int = Field(foreign_key='category.id', primary_key=True)


class CategoryBase(SQLModel):
  name: str = Field(max_length=100, nullable=False)
  color: str


class CategoryCreate(CategoryBase):
  @field_validator('color', mode='before')
  def validate_and_convert_color(cls, v):
    if isinstance(v, Color):

      return v.as_hex()
    elif isinstance(v, str):
      try:
        c = Color(v)

        return c.as_hex()
      except Exception:
        raise ValueError('Invalid color string')
    raise ValueError('color must be a string or Color instance')

class CategoryPub(CategoryBase):
  id: int


class CategoriesPub(SQLModel):
  data: list[CategoryPub]


class Category(CategoryBase, table=True):
  id: int | None = Field(default=None, primary_key=True)

  transactions: list["Transaction"] = Relationship(
    back_populates='categories',
    link_model=TransactionsCategoriesLink,
  )
