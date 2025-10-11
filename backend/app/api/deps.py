from collections.abc import Generator
from typing import Annotated

import jwt
import redis.asyncio as redis
from app.core import security
from app.core.database import engine, get_db
from app.core.redis import get_redis
from app.core.settings import settings
from app.models.users import TokenPayload, User
from fastapi import Depends, HTTPException, Request, status
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(get_token_from_cookie)]
RedisDep = Annotated[redis.Redis, Depends(get_redis)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # commented til account activation will not be realised
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    return current_user


is_superuser = Depends(get_current_active_superuser)
