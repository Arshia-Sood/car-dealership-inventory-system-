import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.user import User, UserRole


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def get_auth_headers(client: TestClient, role: UserRole = UserRole.USER) -> dict:
    unique = uuid.uuid4().hex[:8]
    email = f"inv_{role.value}_{unique}@example.com"
    password = "password123"
    username = f"inv_user_{unique}"

    res = client.post(
        "/api/auth/register",
        json={"email": email, "username": username, "password": password},
    )
    assert res.status_code == 201

    if role == UserRole.ADMIN:
        with SessionLocal() as session:
            user = session.query(User).filter(User.email == email).first()
            user.role = UserRole.ADMIN
            session.commit()

    login_res = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    return {"Authorization": f"Bearer {login_res.json()['access_token']}"}


def create_vehicle(client: TestClient, headers: dict, quantity_in_stock: int = 10) -> dict:
    res = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000.0,
            "quantity_in_stock": quantity_in_stock,
        },
        headers=headers,
    )
    assert res.status_code == 201
    return res.json()


@pytest.fixture
def admin_headers(client: TestClient) -> dict:
    return get_auth_headers(client, role=UserRole.ADMIN)


@pytest.fixture
def user_headers(client: TestClient) -> dict:
    return get_auth_headers(client, role=UserRole.USER)


# ─────────────────────────────────────────────────────────────────────────────
# Purchase  POST /api/vehicles/{id}/purchase
# ─────────────────────────────────────────────────────────────────────────────

class TestVehiclePurchaseAuth:
    def test_unauthenticated_purchase_returns_401(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", json={"quantity": 1})

        assert response.status_code == 401

    def test_normal_user_can_purchase(self, client: TestClient, admin_headers: dict, user_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 2},
            headers=user_headers,
        )

        assert response.status_code == 200

    def test_admin_can_purchase(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 3},
            headers=admin_headers,
        )

        assert response.status_code == 200


class TestVehiclePurchaseSuccess:
    def test_purchase_reduces_stock(self, client: TestClient, admin_headers: dict, user_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 4},
            headers=user_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity_in_stock"] == 6

    def test_purchase_entire_stock(self, client: TestClient, admin_headers: dict, user_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 5},
            headers=user_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity_in_stock"] == 0

    def test_purchase_response_contains_vehicle_fields(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 1},
            headers=user_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "make" in data
        assert "model" in data
        assert "category" in data
        assert "price" in data
        assert "quantity_in_stock" in data


class TestVehiclePurchaseErrors:
    def test_purchase_exceeds_stock_returns_400(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=3)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 10},
            headers=user_headers,
        )

        assert response.status_code == 400

    def test_purchase_zero_quantity_returns_422(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": 0},
            headers=user_headers,
        )

        assert response.status_code == 422

    def test_purchase_negative_quantity_returns_422(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={"quantity": -5},
            headers=user_headers,
        )

        assert response.status_code == 422

    def test_purchase_missing_quantity_returns_422(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=10)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/purchase",
            json={},
            headers=user_headers,
        )

        assert response.status_code == 422

    def test_purchase_non_existent_vehicle_returns_404(
        self, client: TestClient, user_headers: dict
    ):
        response = client.post(
            "/api/vehicles/999999/purchase",
            json={"quantity": 1},
            headers=user_headers,
        )

        assert response.status_code == 404


# ─────────────────────────────────────────────────────────────────────────────
# Restock  POST /api/vehicles/{id}/restock
# ─────────────────────────────────────────────────────────────────────────────

class TestVehicleRestockAuth:
    def test_unauthenticated_restock_returns_401(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"quantity": 10})

        assert response.status_code == 401

    def test_normal_user_restock_returns_403(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 10},
            headers=user_headers,
        )

        assert response.status_code == 403

    def test_admin_can_restock(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 10},
            headers=admin_headers,
        )

        assert response.status_code == 200


class TestVehicleRestockSuccess:
    def test_restock_increases_stock(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 10},
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity_in_stock"] == 15

    def test_restock_from_zero(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=0)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 20},
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["quantity_in_stock"] == 20

    def test_restock_response_contains_vehicle_fields(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 10},
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "make" in data
        assert "model" in data
        assert "category" in data
        assert "price" in data
        assert "quantity_in_stock" in data


class TestVehicleRestockErrors:
    def test_restock_zero_quantity_returns_422(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": 0},
            headers=admin_headers,
        )

        assert response.status_code == 422

    def test_restock_negative_quantity_returns_422(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={"quantity": -1},
            headers=admin_headers,
        )

        assert response.status_code == 422

    def test_restock_missing_quantity_returns_422(self, client: TestClient, admin_headers: dict):
        vehicle = create_vehicle(client, admin_headers, quantity_in_stock=5)

        response = client.post(
            f"/api/vehicles/{vehicle['id']}/restock",
            json={},
            headers=admin_headers,
        )

        assert response.status_code == 422

    def test_restock_non_existent_vehicle_returns_404(self, client: TestClient, admin_headers: dict):
        response = client.post(
            "/api/vehicles/999999/restock",
            json={"quantity": 10},
            headers=admin_headers,
        )

        assert response.status_code == 404
