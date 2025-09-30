import pytest


pytestmark = [pytest.mark.integration, pytest.mark.endpoints]


def test_get_all_categories(auth_client, categories):
  response = auth_client.get("/api/v1/categories/")

  body = response.json()
  assert response.status_code == 200
  assert len(body["data"]) == 2


def test_not_admin_create_category(auth_client):
  post_body = {
    "name": "Test Category",
    "color": "#FFFD75",
  }
  response = auth_client.post("/api/v1/categories/", json=post_body)

  assert response.status_code >= 400


def test_create_new_category(auth_admin_client):
  post_body = {
    "name": "Test Category",
    "color": "yellow",
  }
  response = auth_admin_client.post("/api/v1/categories/", json=post_body)

  body = response.json()
  assert response.status_code == 200
  assert body["name"] == "Test Category"
  assert body["color"] == "#ff0"
