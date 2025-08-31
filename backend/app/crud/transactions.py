from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.transactions import Transaction, TransactionsPub, TransactionCreate
from app.models.wallets import Wallet
from app.models.categories import Category

def create_transaction(*, session: Session, transaction: TransactionCreate) -> Transaction:
  new_transaction = Transaction(**transaction.model_dump(exclude={"categories"}))

  if transaction.categories:
    categories = session.exec(
      select(Category).where(Category.id.in_(transaction.categories))
    ).all()

    if len(categories) != len(transaction.categories):
      raise HTTPException(status_code=400, detail="Some categories not found")

    new_transaction.categories = categories

  session.add(new_transaction)
  session.commit()
  session.refresh(new_transaction)

  return new_transaction


def get_transactions_by_wallet(*, session: Session, wallet_id: Wallet.id) -> TransactionsPub:
  q = select(Transaction).where(Transaction.wallet_id == wallet_id)
  transactions = session.exec(q).all()

  return TransactionsPub(data=transactions, count=len(transactions))
  