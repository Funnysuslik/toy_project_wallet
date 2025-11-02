from typing import Any

from app.api.deps import CurrentUser, SessionDep
from app.crud.wallets import create_wallet, get_wallets_by_user
from app.models.wallets import WalletCreate, WalletPublic, WalletsPublic
from fastapi import APIRouter

wallets_router = APIRouter(prefix="/wallets", tags=["wallets"])


@wallets_router.get("", response_model=WalletsPublic)
async def get_all_user_wallets(session: SessionDep, user: CurrentUser) -> Any:
    """Get all current user wallets."""
    return await get_wallets_by_user(session=session, user=user)


@wallets_router.post("", response_model=WalletPublic)
async def create_wallet_endpoint(session: SessionDep, user: CurrentUser, wallet: WalletCreate) -> Any:
    """Create a new wallet for current user."""
    new_wallet = await create_wallet(session=session, wallet=wallet, user=user)

    return WalletPublic.model_validate(new_wallet)
