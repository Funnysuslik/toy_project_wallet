from typing import Any

from app.api.deps import SessionDep
from app.crud.transactions import create_transaction, get_transactions_by_wallet
from app.models.transactions import Transaction, TransactionCreate, TransactionsPub
from fastapi import APIRouter

transactions_router = APIRouter(prefix="/transactions", tags=["transactions"])


@transactions_router.get("", response_model=TransactionsPub)
async def get_all_wallet_transactions(session: SessionDep, wallet_id: int) -> Any:
    """Get all transactions by wallet."""
    return await get_transactions_by_wallet(session=session, wallet_id=wallet_id)


@transactions_router.post("", response_model=Transaction)
async def create_transaction_endpiont(session: SessionDep, transaction: TransactionCreate) -> Any:
    """Create a new transaction."""
    new_transaction = await create_transaction(session=session, transaction=transaction)

    return new_transaction
