import uuid
from enum import Enum as PyEnum

from pydantic import EmailStr, model_validator  # , SecretStr
from sqlalchemy import Enum as SAEnum
from sqlmodel import Column, Field, Relationship, SQLModel


class UserRole(str, PyEnum):
    user = "user"
    admin = "admin"
    troll = "troll"


class Token(SQLModel):
    """Token model."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    """Token payload model."""

    sub: str | None = None


class UserBase(SQLModel):
    """User base model."""

    name: str | None = Field(default=None, max_length=50)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    role: UserRole = Field(
        default=UserRole.user,
        sa_column=Column(
            SAEnum(UserRole, name="user_role_enum"),
            nullable=False,
        ),
    )


class UserPublic(UserBase):
    """User public model."""

    id: uuid.UUID


class UsersPublic(SQLModel):
    """Users public model."""

    data: list[UserPublic]
    count: int


class UserCreate(UserBase):
    """User create model."""

    password: str = Field(min_length=8, max_length=40)
    password_check: str

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        if values.get("password") != values.get("password_check"):
            raise ValueError("passwords do not match")

        return values


class UserCreateGoogle(UserBase):
    """User create google model."""

    google_id: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=True)

    wallets: list["Wallet"] = Relationship(back_populates="user", cascade_delete=True)
