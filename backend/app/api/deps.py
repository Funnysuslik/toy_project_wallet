from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from app.core.database import engine
from app.models.users import User
from app.crud.users import get_user_by_email

security = HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db)
) -> User:
    # TODO: Implement proper JWT token validation
    # For now, we'll use a simple email-based lookup
    # In a real implementation, you'd decode the JWT token and extract user info
    
    # Placeholder: extract email from token (this should be JWT decoding)
    email = credentials.credentials  # This is just a placeholder
    
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
