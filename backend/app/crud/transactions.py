from app.models.categories import Category
from app.models.transactions import (
    Transaction,
    TransactionCreate,
    TransactionPub,
    TransactionsPub,
)
from app.models.wallets import Wallet
from fastapi import HTTPException
from sqlmodel import Session, select


def create_transaction(*, session: Session, transaction: TransactionCreate) -> Transaction:
    """Create a new transaction."""
    new_transaction = Transaction(**transaction.model_dump(exclude={"categories"}))

    if transaction.categories:
        categories = session.exec(select(Category).where(Category.id.in_(transaction.categories))).all()

        if len(categories) != len(transaction.categories):
            raise HTTPException(status_code=400, detail="Some categories not found")

        new_transaction.categories = categories

    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    return new_transaction


def get_transactions_by_wallet(*, session: Session, wallet_id: Wallet.id) -> TransactionsPub:
    """Get transactions by wallet."""
    q = select(Transaction).where(Transaction.wallet_id == wallet_id)
    transactions = session.exec(q).all()

    transaction_pubs = []
    for transaction in transactions:
        transaction_pub = TransactionPub(
            id=transaction.id,
            name=transaction.name,
            value=transaction.value,
            date=transaction.date,
            categories=transaction.category_ids,
        )
        transaction_pubs.append(transaction_pub)

    return TransactionsPub(data=transaction_pubs, count=len(transaction_pubs))
