from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.models.users import User, UserCreate, UserPublic, UsersPublic
from app.api.deps import SessionDep
from app.crud.users import get_user_by_email, create_user


users_router = APIRouter(prefix='/users', tags=['users'])

@users_router.get(
  '/',
  response_model=UsersPublic
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
  count_query = select(func.count()).select_from(User)
  count = session.exec(count_query).one()

  query = select(User).offset(skip).limit(limit)
  users = session.exec

  return UsersPublic(users, count=count)

@users_router.post(
  '/',
  response_model=UserPublic,
)
def create_user_endpoint(session: SessionDep, user: UserCreate) -> Any:
  new_user = get_user_by_email(session=session, email=user.email)
  if new_user:
    raise HTTPException(
      status_code=400,
      detail="The user with this email already exists in the system.",
    )

  new_user = create_user(session=session, user_create=user)
  
  return UserPublic.model_validate(new_user)
