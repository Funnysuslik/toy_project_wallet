from app.core.security import get_password_hash, verify_password
from app.models.users import User, UserCreate
from sqlmodel import Session, select


def create_user(*, session: Session, user: UserCreate) -> User:
    new_user = User.model_validate(user, update={"hashed_password": get_password_hash(user.password)})
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    q = select(User).where(User.email == email)
    user = session.exec(q).first()
    return user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
