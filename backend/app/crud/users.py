from app.core.security import get_password_hash, verify_password
from app.models.users import User, UserCreate
from sqlmodel import Session, select


async def create_user(*, session: Session, user: UserCreate) -> User:
    """Create a new user."""
    new_user = User.model_validate(user, update={"hashed_password": get_password_hash(user.password)})
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Get a user by email."""
    user = await session.execute(select(User).where(User.email == email)).scalars().first()

    return user


async def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate a user."""
    user = await get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
