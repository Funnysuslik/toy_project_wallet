from app.models.users import User
from app.models.wallets import Wallet, WalletCreate, WalletsPublic
from sqlmodel import Session, select


def create_wallet(*, session: Session, wallet: WalletCreate, user: User) -> Wallet:
    wallet_data = wallet.model_dump()
    wallet_data["user_id"] = user.id

    new_wallet = Wallet.model_validate(wallet_data)
    session.add(new_wallet)
    session.commit()
    session.refresh(new_wallet)

    return new_wallet


def get_wallets_by_user(*, session: Session, user: User) -> WalletsPublic:
    q = select(Wallet).where(Wallet.user_id == user.id)
    wallets = session.exec(q).all()

    return WalletsPublic(data=wallets, count=len(wallets))
