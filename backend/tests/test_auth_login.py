import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def registered_user_credentials(client: TestClient) -> dict:
    """Helper fixture/function to create a valid registered user for login tests."""
    unique = uuid.uuid4().hex[:8]
    payload = {
        "email": f"login_{unique}@example.com",
        "username": f"login_{unique}",
        "password": "securepassword123",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    return payload


class TestLoginSuccess:
    def test_login_success_returns_jwt_token(self, client: TestClient):
        user_data = registered_user_credentials(client)
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        response = client.post("/api/auth/login", json=login_payload)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
        assert data.get("token_type") == "bearer"


class TestLoginAuthenticationErrors:
    def test_login_nonexistent_email_returns_401(self, client: TestClient):
        login_payload = {
            "email": "nonexistent_user@example.com",
            "password": "somepassword123",
        }

        response = client.post("/api/auth/login", json=login_payload)

        assert response.status_code == 401

    def test_login_incorrect_password_returns_401(self, client: TestClient):
        user_data = registered_user_credentials(client)
        login_payload = {
            "email": user_data["email"],
            "password": "wrongpassword123",
        }

        response = client.post("/api/auth/login", json=login_payload)

        assert response.status_code == 401


class TestLoginValidationErrors:
    def test_login_missing_email_returns_422(self, client: TestClient):
        login_payload = {"password": "securepassword123"}

        response = client.post("/api/auth/login", json=login_payload)

        assert response.status_code == 422

    def test_login_missing_password_returns_422(self, client: TestClient):
        login_payload = {"email": "user@example.com"}

        response = client.post("/api/auth/login", json=login_payload)

        assert response.status_code == 422

    def test_login_invalid_request_body_returns_422(self, client: TestClient):
        response = client.post("/api/auth/login", json="invalid_json_body")

        assert response.status_code == 422
