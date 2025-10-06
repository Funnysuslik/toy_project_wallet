from app.core.settings import settings
from sqlmodel import create_engine

engine = create_engine(str(settings.DATABASE_URI))
