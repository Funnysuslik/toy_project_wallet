from datetime import datetime

from app.models.categories import TransactionsCategoriesLink
from sqlmodel import Field, Relationship, SQLModel


class BaseTransaction(SQLModel):
    """Base transaction model."""

    value: float = Field(default=0.0)
    name: str = Field(default="", max_length=100)
    date: datetime = Field(default_factory=datetime.now)


class TransactionCreate(BaseTransaction):
    """Transaction creation model."""

    wallet_id: int
    categories: list[int]


class TransactionPub(BaseTransaction):
    """Transaction public model."""

    id: int
    categories: list[int]

    class Config:
        from_attributes = True


class TransactionsPub(SQLModel):
    """Transactions public model."""

    data: list[TransactionPub]
    count: int


class Transaction(BaseTransaction, table=True):
    """Transaction model."""

    id: int | None = Field(default=None, primary_key=True)
    wallet_id: int = Field(foreign_key="wallet.id")

    categories: list["Category"] = Relationship(back_populates="transactions", link_model=TransactionsCategoriesLink)

    @property
    def category_ids(self) -> list[int]:
        """Get the category ids for the transaction."""
        return [c.id for c in self.categories]
