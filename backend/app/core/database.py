from app.core.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(str(settings.DATABASE_URI))
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Get a database session."""
    async with new_session() as session:
        yield session
