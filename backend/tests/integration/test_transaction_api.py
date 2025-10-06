import pytest

pytestmark = [pytest.mark.integration, pytest.mark.endpoints]


def test_create_transaction_api(client, wallet):
    post_body = {
        "wallet_id": wallet.id,
        "name": "Groceries",
        "value": 100.0,
        "categories": [],
    }
    response = client.post("/api/v1/transactions/", json=post_body)
    assert response.status_code == 200

    body = response.json()
    assert body["name"] == post_body["name"]
    assert body["wallet_id"] == wallet.id
    assert body["value"] == 100.0


def test_get_transactions_by_wallet(client, wallet, transactions):
    response = client.get(f"/api/v1/transactions?wallet_id={wallet.id}")

    body = response.json()
    assert body["count"] == len(transactions)
    assert sorted(t["name"] for t in body["data"]) == sorted(t.name for t in transactions)
