from datetime import datetime

from sqlmodel import SQLModel, Field


class BaseTransaction(SQLModel):
  value: float = Field(nullable=False, default=0.0)
  name: str = Field(nullable=False, default='', max_length=100)


class TransactionCreate(BaseTransaction):
  wallet_id: int


class TransactionPub(BaseTransaction):
  date: datetime


class TransactionsPub(SQLModel):
  data: list[TransactionPub]
  count: int


class Transaction(BaseTransaction, table=True):
  id: int | None = Field(default=1, primary_key=True)
  date: datetime = Field(nullable=False, default=datetime.now())
  wallet_id: int = Field(foreign_key='wallet.id', nullable=False)
