from sqlmodel import Session, select

from app.models.wallets import Wallet, WalletCreate, WalletsPublic
from app.models.users import User


def create_wallet(*, session: Session, wallet_create_data: WalletCreate, user: User) -> Wallet:
  wallet_data = wallet_create_data.model_dump()
  wallet_data['user_id'] = user.id

  wallet = Wallet.model_validate(wallet_data)
  session.add(wallet)
  session.commit()
  session.refresh(wallet)

  return wallet


def get_wallets_by_user(*, session: Session, user: User) -> WalletsPublic:
  q = select(Wallet).where(Wallet.user_id == user.id)
  wallets = session.exec(q).all()

  return WalletsPublic(data=wallets, count=len(wallets))
