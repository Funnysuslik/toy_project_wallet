from pathlib import Path
import sys
import os
import tempfile

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from datetime import datetime
from sqlmodel import create_engine, Session, SQLModel


backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
  sys.path.insert(0, str(backend_dir))


from app.main import app
from app.api.deps import get_db, get_current_user
from app.models.categories import Category
from app.models.transactions import Transaction
from app.models.wallets import Wallet
from app.models.users import User


@pytest.fixture(scope="function")
def engine():
  fd, path = tempfile.mkstemp(suffix=".db")
  os.close(fd)
  engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
  
  SQLModel.metadata.create_all(engine)
  yield engine
  engine.dispose()
  os.remove(path)


@pytest.fixture(scope="function")
def session(engine):
  with Session(engine) as session:
    yield session

@pytest.fixture(scope="function")
def client(engine):
  def _get_test_db():
    with Session(engine) as s:
      yield s

  app.dependency_overrides[get_db] = _get_test_db

  with TestClient(app) as c:
    yield c

  app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def faker():
  return Faker()


@pytest.fixture
def user(session):
  """Create a reusable user for tests"""
  u = User(name="Test User", email="user@test.com", is_active=True, hashed_password="hashedpassword")
  session.add(u)
  session.commit()
  session.refresh(u)
  return u


@pytest.fixture
def auth_client(client, user):
  """Create reusable authorized client"""
  app.dependency_overrides[get_current_user] = lambda: user
  try:
    yield client
  finally:
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def admin(session):
  """Create a reusable user for tests"""
  u = User(name="Test User", email="user@test.com", is_active=True, is_superuser=True, hashed_password="hashedpassword")
  session.add(u)
  session.commit()
  session.refresh(u)
  return u


@pytest.fixture
def super_auth_client(client, admin):
  """Create reusable authorized as admin client"""
  app.dependency_overrides[get_current_user] = lambda: admin
  try:
    yield client
  finally:
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def wallet(session, user):
  """Create a reusable wallet for tests"""
  w = Wallet(name="Test Wallet", type="debit", user_id=user.id)
  session.add(w)
  session.commit()
  session.refresh(w)
  return w


@pytest.fixture
def categories(session):
  """Create reusable categories for tests"""
  c1 = Category(name="Food", color="FFFFFF")
  c2 = Category(name="Rent", color="000000")
  session.add_all([c1, c2])
  session.commit()
  session.refresh(c1)
  session.refresh(c2)
  return [c1, c2]


@pytest.fixture
def transactions(session, wallet, categories):
  """Create reusable transactions for tests"""
  t1 = Transaction(name="Test transaction 1", wallet_id=wallet.id, categories=categories)
  t2 = Transaction(name="Test transaction 2", wallet_id=wallet.id, categories=[])
  session.add_all([t1, t2])
  session.commit()
  session.refresh(t1)
  session.refresh(t2)
  return [t1, t2]


@pytest.fixture
def now():
  return datetime.now(datetime.timezone.utc)
