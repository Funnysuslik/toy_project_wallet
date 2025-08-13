from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
# from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from app.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# config = AuthXConfig()
# config.JWT_SECRET_KEY = settings.SECRET_KEY
# config.JWT_ACCESS_COOKIE_NAME = 'access_token'
# config.JWT_TOKEN_LOCATION = ['cookies']
# config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

# security = AuthX(config=config)

ALGORITHM = "HS256"

def create_jwt_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)