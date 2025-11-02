import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel  # , Session, create_engine

backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_session
from app.main import app
from app.models.categories import Category
from app.models.transactions import Transaction
from app.models.users import User
from app.models.wallets import Wallet


@pytest_asyncio.fixture(scope="function")
async def engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_async_engine(f"sqlite+aiosqlite:///{path}", connect_args={"check_same_thread": False})

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()
    os.remove(path)


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    new_session = async_sessionmaker(engine, expire_on_commit=False)
    async with new_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(engine):
    async def _get_test_db():
        new_session = async_sessionmaker(engine, expire_on_commit=False)
        async with new_session() as session:
            yield session

    app.dependency_overrides[get_session] = _get_test_db

    test_client = TestClient(
        app,
        base_url="http://testserver",
        raise_server_exceptions=True,
        root_path="",
        backend="asyncio",
        backend_options=None,
        cookies=None,
        headers=None,
        follow_redirects=True,
        client=("testclient", 50000),
    )
    with test_client as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(session):
    """Create a reusable user for tests"""
    u = User(
        name="Test User",
        email="user@test.com",
        is_active=True,
        hashed_password="hashedpassword",
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def auth_client(client, user):
    """Create reusable authorized client"""
    app.dependency_overrides[get_current_user] = lambda: user
    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_current_user, None)


@pytest_asyncio.fixture
async def admin(session):
    """Create a reusable user for tests"""
    u = User(
        name="Test Admin",
        email="admin@test.com",
        is_active=True,
        is_superuser=True,
        hashed_password="hashedpassword",
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@pytest_asyncio.fixture
async def auth_admin_client(client, admin):
    """Create reusable authorized as admin client"""
    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[get_current_active_superuser] = lambda: admin
    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_current_user, None)
        app.dependency_overrides.pop(get_current_active_superuser, None)


@pytest_asyncio.fixture
async def wallet(session, user):
    """Create a reusable wallet for tests"""
    w = Wallet(name="Test Wallet", type="debit", user_id=user.id)
    session.add(w)
    await session.commit()
    await session.refresh(w)
    return w


@pytest_asyncio.fixture
async def categories(session):
    """Create reusable categories for tests"""
    c1 = Category(name="Food", color="#FFFFFF")
    c2 = Category(name="Rent", color="#000")
    session.add_all([c1, c2])
    await session.commit()
    await session.refresh(c1)
    await session.refresh(c2)
    return [c1, c2]


@pytest_asyncio.fixture
async def transactions(session, wallet, categories):
    """Create reusable transactions for tests"""
    t1 = Transaction(name="Test transaction 1", wallet_id=wallet.id, categories=categories)
    t2 = Transaction(name="Test transaction 2", wallet_id=wallet.id, categories=[])
    session.add_all([t1, t2])
    await session.commit()
    await session.refresh(t1)
    await session.refresh(t2)
    return [t1, t2]


@pytest_asyncio.fixture
def now():
    return datetime.now(datetime.timezone.utc)
