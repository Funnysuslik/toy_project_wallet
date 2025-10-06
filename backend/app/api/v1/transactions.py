from typing import Any

# from app.models.wallets import Wallet
from app.api.deps import SessionDep
from app.crud.transactions import create_transaction, get_transactions_by_wallet
from app.models.transactions import Transaction, TransactionCreate, TransactionsPub
from fastapi import APIRouter

transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])


@transactions_router.get("", response_model=TransactionsPub)
def get_all_wallet_transactions(session: SessionDep, wallet_id: int, variables: dict) -> Any:

    return get_transactions_by_wallet(session=session, wallet_id=wallet_id, variables=variables)


@transactions_router.post("", response_model=Transaction)
def create_transaction_endpiont(session: SessionDep, transaction: TransactionCreate) -> Any:
    new_transaction = create_transaction(session=session, transaction=transaction)

    return Transaction.model_validate(new_transaction)
