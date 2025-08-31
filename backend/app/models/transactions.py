from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field

from app.models.categories import TransactionsCategoriesLink


class BaseTransaction(SQLModel):
  value: float = Field(nullable=False, default=0.0)
  name: str = Field(nullable=False, default='', max_length=100)
  date: datetime | None = Field(nullable=False, default=datetime.now())


class TransactionCreate(BaseTransaction):
  wallet_id: int
  categories: list[int]


class TransactionPub(BaseTransaction):
  id: int
  categories: list[int]

  class Config:
      from_attributes = True


class TransactionsPub(SQLModel):
  data: list[TransactionPub]
  count: int


class Transaction(BaseTransaction, table=True):
  id: int | None = Field(default=None, primary_key=True)
  date: datetime | None = Field(nullable=False, default=datetime.now())
  wallet_id: int = Field(foreign_key='wallet.id', nullable=False)

  categories: list["Category"] = Relationship(
    back_populates='transactions',
    link_model=TransactionsCategoriesLink
  )

  @property
  def category_ids(self) -> list[int]:

    return [c.id for c in self.categories]
