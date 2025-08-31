from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import func, select

from app.models.users import Token, User, UserCreate, UserPublic, UsersPublic
from app.api.deps import CurrentUser, SessionDep, is_superuser
from app.crud.users import authenticate, get_user_by_email, create_user
from app.core import security
from app.core.settings import settings


users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get(
  '/',
  response_model=UsersPublic,
  dependencies=[is_superuser],
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
  count_query = select(func.count()).select_from(User)
  count = session.exec(count_query).one()

  query = select(User).offset(skip).limit(limit)
  users = session.exec(query).all()

  return UsersPublic(data=users, count=count)


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

  new_user = create_user(session=session, user=user)

  return UserPublic.model_validate(new_user)


@users_router.post("/login/access-token")
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> Token:
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # commented till account activation will not be implemented
    # elif not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_jwt_token(user.id, expires_delta=access_token_expires)

    response.set_cookie(
        'access_token',
        access_token,
        httponly=True,
        secure=False,  # False для разработки (HTTP), True для продакшена (HTTPS)
        samesite='lax',
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return Token(access_token=access_token)


@users_router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:

    return current_user


@users_router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie("access_token", secure=False, httponly=True, samesite='lax')

    return {"message": "Successfully logged out"}
