from sqlmodel import Session, create_engine, select

from app.core.settings import settings


engine = create_engine(str(settings.DATABASE_URI))