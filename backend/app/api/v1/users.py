from datetime import timedelta
from typing import Annotated, Any

from aiohttp import ClientSession
from app.api.deps import CurrentUser, SessionDep, is_superuser
from app.core import security
from app.core.settings import settings
from app.crud.users import (
    authenticate,
    create_user,
    create_user_google,
    get_user_by_email,
    get_user_by_google_id,
)
from app.models.users import (
    Token,
    User,
    UserCreate,
    UserCreateGoogle,
    UserPublic,
    UsersPublic,
)
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import func, select

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    "",
    response_model=UsersPublic,
    dependencies=[is_superuser],
)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Get all users."""
    count_query = select(func.count()).select_from(User)
    count_result = await session.execute(count_query)
    count = count_result.one()[0]

    query = select(User).offset(skip).limit(limit)
    result = await session.execute(query)
    users = result.scalars().all()

    return UsersPublic(data=users, count=count)


@users_router.post(
    "/",
    response_model=UserPublic,
)
async def create_user_endpoint(session: SessionDep, user: UserCreate) -> Any:
    """Create a new user."""
    new_user = await get_user_by_email(session=session, email=user.email)
    if new_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    new_user = await create_user(session=session, user=user)

    return UserPublic.model_validate(new_user)


@users_router.post("/login/access-token")
async def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> Token:
    """Login a user."""
    user = await authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # commented till account activation will not be implemented
    # elif not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_jwt_token(user.id, expires_delta=access_token_expires)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=False,  # False для разработки (HTTP), True для продакшена (HTTPS)
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return Token(access_token=access_token)


@users_router.get("/login/google/callback")
async def google_callback(request: Request, session: SessionDep, response: Response):
    """Google callback."""
    code = request.query_params.get("code")
    async with ClientSession() as client_session:
        async with client_session.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
        ) as resp:
            if not resp.ok:
                raise HTTPException(status_code=400, detail=f"Failed to get Google token: {resp.text}, code: {code}")
            data = await resp.json()
            access_token = data["access_token"]
            user_info = await client_session.get(
                url="https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if not user_info.ok:
                raise HTTPException(status_code=400, detail="Failed to get Google user info")
            user_info_data = await user_info.json()
            google_id = user_info_data["id"]
            user = await get_user_by_google_id(session=session, google_id=google_id)
            if not user:
                user = await create_user_google(
                    session=session,
                    user=UserCreateGoogle(
                        google_id=google_id, email=user_info_data["email"], name=user_info_data["name"]
                    ),
                )

            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = security.create_jwt_token(user.id, expires_delta=access_token_expires)

            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=False,  # False для разработки (HTTP), True для продакшена (HTTPS)
                samesite="lax",
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )

            return RedirectResponse(url=settings.FRONTEND_HOST + "/welcome", status_code=302)


@users_router.post("/me", response_model=UserPublic)
def get_current_user(current_user: CurrentUser) -> Any:
    """Get the current user."""
    return current_user


@users_router.post("/logout")
def logout(response: Response) -> dict:
    """Logout a current user."""
    response.delete_cookie("access_token", secure=False, httponly=True, samesite="lax")

    return {"message": "Successfully logged out"}
