import pytest
from fastapi import HTTPException

from app.crud.transactions import create_transaction, get_transactions_by_wallet
from app.models.transactions import TransactionCreate


pytestmark = [pytest.mark.integration, pytest.mark.crud]


def test_create_transaction_with_categories(session, wallet, categories):
  data = TransactionCreate(
    wallet_id=wallet.id,
    name="Grocery Shopping",
    value=50.0,
    categories=[c.id for c in categories]
  )

  tx = create_transaction(session=session, transaction=data)

  assert tx.id is not None
  assert tx.name == "Grocery Shopping"
  assert tx.value == 50.0
  assert tx.wallet_id == wallet.id
  assert sorted([c.id for c in tx.categories]) == sorted([c.id for c in categories])


def test_create_transaction_without_categories(session, wallet):
  data = TransactionCreate(
    wallet_id=wallet.id,
    name="No Category Tx",
    value=20.0,
    categories=[]
  )

  tx = create_transaction(session=session, transaction=data)

  assert tx.id is not None
  assert tx.categories == []


def test_create_transaction_invalid_category(session, wallet):
  data = TransactionCreate(
    wallet_id=wallet.id,
    name="Invalid Category Tx",
    value=10.0,
    categories=[999]
  )

  with pytest.raises(HTTPException) as exc:
    create_transaction(session=session, transaction=data)

  assert exc.value.status_code == 400
  assert exc.value.detail == "Some categories not found"


def test_get_all_transactions_by_wallet(session, wallet, transactions):
  ts = get_transactions_by_wallet(session=session, wallet_id=wallet.id)

  assert ts.count == 2
  assert sorted(t.name for t in ts.data) == sorted(t.name for t in transactions)