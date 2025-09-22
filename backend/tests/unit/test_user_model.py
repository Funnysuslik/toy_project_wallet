import pytest

from app.models.users import UserCreate


def test_user_create_with_nonmatching_passwords():
  with pytest.raises(ValueError):
    UserCreate(name='Test user', email='user@test.com', password='qwerty1234', password_check='1234qwerty')


def test_user_create_returns_instanse_after_validation():
  u = UserCreate(name='Test user', email='user@test.com', password='qwerty1234', password_check='qwerty1234')

  assert isinstance(u, UserCreate)