import pytest


def test_create_user(client):
    """Test creating a new user."""
    post_body = {
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword",
        "password_check": "testpassword",
    }
    response = client.post("/api/v1/users", json=post_body)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Test User"

    fail_response = client.post("/api/v1/users", json=post_body)
    assert fail_response.status_code >= 400


def test_get_users_not_admin(auth_client):
    """Test getting users when not an admin."""
    response = auth_client.get("/api/v1/users")

    assert response.status_code >= 200


def test_get_users_admin(auth_admin_client, user):
    """Test getting users when an admin."""
    response = auth_admin_client.get("/api/v1/users")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["data"][0]["name"] == "Test Admin"
