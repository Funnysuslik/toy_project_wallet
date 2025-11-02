import pytest

pytestmark = [pytest.mark.integration, pytest.mark.endpoints, pytest.mark.asyncio]


async def test_get_all_user_wallets(auth_client, wallet):
    """Test getting all user wallets."""
    response = auth_client.get("/api/v1/wallets")

    body = response.json()
    assert response.status_code == 200
    assert body["count"] == 1
    assert any(w["id"] == wallet.id for w in body["data"])


async def test_create_wallet(auth_client):
    """Test creating a new wallet."""
    post_body = {
        "name": "Test New Wallet",
        "type": "debit",
        "currency": "USD",
    }
    response = auth_client.post("/api/v1/wallets", json=post_body)

    body = response.json()
    assert response.status_code == 200
    assert body["name"] == "Test New Wallet"
    assert "id" in body
