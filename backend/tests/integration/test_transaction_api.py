import pytest


pytestmark = [pytest.mark.integration, pytest.mark.endpoints]


def test_create_transaction_api(client, wallet):
  tx_data = {"wallet_id": wallet.id, "name": "Groceries", "value": 100.0, "categories": []}
  response = client.post("/api/v1/transactions/", json=tx_data)
  assert response.status_code == 200

  body = response.json()
  assert body["name"] == tx_data["name"]
  assert body["wallet_id"] == wallet.id
  assert body["value"] == 100.0


def test_get_transactions_by_wallet(client, wallet, transactions):
  response = client.get(f"/api/v1/transactions/?wallet_id={wallet.id}")

  body = response.json()
  assert body["count"] == len(transactions)
  assert sorted(t["name"] for t in body["data"]) == sorted(t.name for t in transactions)
