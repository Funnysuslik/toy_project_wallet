from collections.abc import Generator

from app.core.settings import settings
from sqlmodel import Session, create_engine

engine = create_engine(str(settings.DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
