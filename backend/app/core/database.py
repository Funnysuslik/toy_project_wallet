from sqlmodel import create_engine

from app.core.settings import settings


engine = create_engine(str(settings.DATABASE_URI))
