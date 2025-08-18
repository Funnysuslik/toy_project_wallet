import uuid
from sqlmodel import SQLModel, Field, Column, Enum


class WalletBase(SQLModel):
  name: str = Field(default='Wallet', max_length=50)
  type: str = Field(
    sa_column = Column(
      Enum('debit', 'credit', name='wallet_type_enum'),
      nullable=False,
    )
  )
  balance: float = Field(
    default=0.0,
    nullable=False
  )
  currency: str = Field(
    default='USD',
    nullable=False
  )


class WalletCreate(WalletBase):
  pass

class WalletPublic(WalletBase):
  id: int
  user_id: uuid.UUID


class WalletsPublic(SQLModel):
  data: list[WalletPublic]
  count: int


class Wallet(WalletBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")
