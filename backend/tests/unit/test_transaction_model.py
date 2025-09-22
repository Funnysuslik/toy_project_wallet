# if i get it right you don't need test models without custom validation e.t.c. if you're using fixtures for other tests
# from datetime import datetime, timedelta
# from types import SimpleNamespace

# import pytest
# from pydantic import ValidationError

# from app.models.transactions import (
#   BaseTransaction,
#   TransactionCreate,
#   Transaction,
# )


# pytestmark = [pytest.mark.unit, pytest.mark.models]


# def test_base_transaction_defaults_now_is_set():
#   bt = BaseTransaction()
#   assert isinstance(bt.value, float)
#   assert bt.value == 0.0
#   assert isinstance(bt.name, str)
#   assert bt.name == ""
#   assert isinstance(bt.date, datetime)
#   assert (datetime.now() - bt.date) < timedelta(seconds=2)


# def test_transactioncreate_validation_raises_on_bad_wallet_id():
#   with pytest.raises(ValidationError):
#     TransactionCreate(wallet_id="not-an-int", categories=[1, 2])


# def test_transactioncreate_validation_raises_on_bad_categories():
#   with pytest.raises(ValidationError):
#     TransactionCreate(wallet_id=1, categories=["a", "b"])


# def test_transaction_creates_with_values():
#   t = TransactionCreate(wallet_id=1, categories=[1, 2], value=123.45, name="pay", date=datetime.now()-timedelta(days=1))


# def test_category_ids_with_categories():
#   """
#   If categories have ids, the property should return them.
#   """
#   fake_tx = SimpleNamespace(categories=[SimpleNamespace(id=1), SimpleNamespace(id=2)])
#   result = Transaction.category_ids.fget(fake_tx)
#   assert result == [1, 2]


# def test_category_ids_empty_list():
#   """
#   If there are no categories, the property should return [].
#   """
#   fake_tx = SimpleNamespace(categories=[])
#   result = Transaction.category_ids.fget(fake_tx)
#   assert result == []
