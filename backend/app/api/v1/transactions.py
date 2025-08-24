from typing import Any
from fastapi import APIRouter

from app.models.transactions import TransactionCreate, TransactionPub, TransactionsPub
# from app.models.wallets import Wallet
from app.api.deps import SessionDep
from app.crud.transactions import get_transactions_by_wallet, create_transaction


transactions_router = APIRouter(prefix='/transactions', tags=['transactions'])


@transactions_router.get(
  '/',
  response_model=TransactionsPub
)
def get_all_wallet_transactions(session: SessionDep, wallet_id: int) -> Any:
  return get_transactions_by_wallet(session=session, wallet_id=wallet_id)


@transactions_router.post(
  '/',
  response_model=TransactionPub
)
def create_transaction_endpiont(session: SessionDep, transaction: TransactionCreate) -> Any:
  new_transaction = create_transaction(session=session, transaction_data=transaction)

  return TransactionPub.model_validate(new_transaction)
