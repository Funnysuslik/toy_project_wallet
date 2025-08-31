from pydantic_extra_types.color import Color
from sqlmodel import Relationship, SQLModel, Field


class TransactionsCategoriesLink(SQLModel, table=True):
  transaction_id: int = Field(foreign_key='transaction.id', primary_key=True)
  category_id: int = Field(foreign_key='category.id', primary_key=True)


class CategoryBase(SQLModel):
  name: str = Field(max_length=100, nullable=False)
  color: str = Field(nullable=False)


class CategoryCreate(CategoryBase):
  color: Color


class CategoryPub(CategoryBase):
  id: int


class CategoriesPub(SQLModel):
  data: list[CategoryPub]


class Category(CategoryBase, table=True):
  id: int = Field(default=1, primary_key=True)
  transaction_id: int 

  transactions: list["Transaction"] = Relationship(
    back_populates='categories',
    link_model=TransactionsCategoriesLink,
  )
