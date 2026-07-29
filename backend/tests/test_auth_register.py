import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def valid_registration_payload(**overrides) -> dict:
    unique = uuid.uuid4().hex[:8]
    payload = {
        "email": f"user_{unique}@example.com",
        "username": f"user_{unique}",
        "password": "securepassword123",
    }
    payload.update(overrides)
    return payload


class TestRegisterSuccess:
    def test_register_returns_201_with_user_details(self, client: TestClient):
        payload = valid_registration_payload()

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == payload["email"]
        assert data["username"] == payload["username"]
        assert data["role"] == "user"
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_does_not_return_password_in_response(self, client: TestClient):
        payload = valid_registration_payload()

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 201
        assert "password" not in response.json()


class TestRegisterValidationErrors:
    def test_register_missing_email_returns_422(self, client: TestClient):
        payload = valid_registration_payload()
        del payload["email"]

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422

    def test_register_missing_username_returns_422(self, client: TestClient):
        payload = valid_registration_payload()
        del payload["username"]

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422

    def test_register_missing_password_returns_422(self, client: TestClient):
        payload = valid_registration_payload()
        del payload["password"]

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422

    def test_register_invalid_email_format_returns_422(self, client: TestClient):
        payload = valid_registration_payload(email="not-an-email")

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422

    def test_register_password_too_short_returns_422(self, client: TestClient):
        payload = valid_registration_payload(password="short")

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422

    def test_register_empty_username_returns_422(self, client: TestClient):
        payload = valid_registration_payload(username="")

        response = client.post("/api/auth/register", json=payload)

        assert response.status_code == 422


class TestRegisterDuplicateErrors:
    def test_register_duplicate_email_returns_409(self, client: TestClient):
        payload = valid_registration_payload()
        first_response = client.post("/api/auth/register", json=payload)
        assert first_response.status_code == 201

        duplicate_payload = valid_registration_payload(
            email=payload["email"],
            username="different_username",
        )
        response = client.post("/api/auth/register", json=duplicate_payload)

        assert response.status_code == 409
        assert "email" in response.json()["detail"].lower()

    def test_register_duplicate_username_returns_409(self, client: TestClient):
        payload = valid_registration_payload()
        first_response = client.post("/api/auth/register", json=payload)
        assert first_response.status_code == 201

        duplicate_payload = valid_registration_payload(
            email="different@example.com",
            username=payload["username"],
        )
        response = client.post("/api/auth/register", json=duplicate_payload)

        assert response.status_code == 409
        assert "username" in response.json()["detail"].lower()
