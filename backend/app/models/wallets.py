import uuid

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


class WalletBase(SQLModel):
    name: str = Field(default="Wallet", max_length=50)
    type: str = Field(
        sa_column=Column(
            Enum("debit", "credit", name="wallet_type_enum"),
        )
    )
    currency: str = Field(default="USD")


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
    user_id: uuid.UUID = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="wallets")
