from typing import Any
from fastapi import APIRouter

from app.api.deps import SessionDep, CurrentUser
from app.crud.wallets import get_wallets_by_user, create_wallet
from app.models.wallets import WalletCreate, WalletsPublic, WalletPublic


wallets_router = APIRouter(prefix='/wallets', tags=['wallets'])


@wallets_router.get(
  '/',
  response_model=WalletsPublic
)
def get_all_user_wallet(session: SessionDep, user: CurrentUser) -> Any:

  return get_wallets_by_user(session=session, user=user)


@wallets_router.post(
  '/',
  response_model=WalletPublic
)
def create_wallet_endpoint(session: SessionDep, user: CurrentUser, wallet: WalletCreate) -> Any:
  new_wallet = create_wallet(session=session, wallet_create_data=wallet, user=user)

  return WalletPublic.model_validate(new_wallet)
