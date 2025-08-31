from sqlmodel import Session, select

from app.models.transactions import Transaction, TransactionsPub, TransactionCreate
from app.models.wallets import Wallet

def create_transaction(*, session: Session, transaction: TransactionCreate) -> Transaction:
  new_transaction = Transaction.model_validate(transaction)
  session.add(new_transaction)
  session.commit()
  session.refresh(new_transaction)

  return new_transaction


def get_transactions_by_wallet(*, session: Session, wallet_id: Wallet.id) -> TransactionsPub:
  q = select(Transaction).where(Transaction.wallet_id == wallet_id)
  transactions = session.exec(q).all()

  return TransactionsPub(data=transactions, count=len(transactions))
  