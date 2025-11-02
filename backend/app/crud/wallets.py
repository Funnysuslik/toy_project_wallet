from app.models.users import User
from app.models.wallets import Wallet, WalletCreate, WalletsPublic
from sqlmodel import Session, select


async def create_wallet(*, session: Session, wallet: WalletCreate, user: User) -> Wallet:
    """Create a new wallet."""
    wallet_data = wallet.model_dump()
    wallet_data["user_id"] = user.id

    new_wallet = Wallet.model_validate(wallet_data)
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)

    return new_wallet


async def get_wallets_by_user(*, session: Session, user: User) -> WalletsPublic:
    """Get wallets by user."""
    result = await session.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallets = result.scalars().all()

    return WalletsPublic(data=wallets, count=len(wallets))
