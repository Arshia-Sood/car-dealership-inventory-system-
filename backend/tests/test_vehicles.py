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
    email = f"veh_{role.value}_{unique}@example.com"
    password = "password123"
    username = f"veh_user_{unique}"

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
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def valid_vehicle_payload(**overrides) -> dict:
    payload = {
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 25000.0,
        "quantity_in_stock": 10,
    }
    payload.update(overrides)
    return payload


class TestVehicleCreate:
    def test_admin_can_create_vehicle(self, client: TestClient):
        headers = get_auth_headers(client, role=UserRole.ADMIN)
        payload = valid_vehicle_payload()

        response = client.post("/api/vehicles", json=payload, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["make"] == payload["make"]
        assert data["model"] == payload["model"]
        assert data["category"] == payload["category"]
        assert data["price"] == payload["price"]
        assert data["quantity_in_stock"] == payload["quantity_in_stock"]

    def test_normal_user_cannot_create_vehicle_returns_403(self, client: TestClient):
        headers = get_auth_headers(client, role=UserRole.USER)
        payload = valid_vehicle_payload()

        response = client.post("/api/vehicles", json=payload, headers=headers)

        assert response.status_code == 403

    def test_unauthenticated_cannot_create_vehicle_returns_401(self, client: TestClient):
        payload = valid_vehicle_payload()

        response = client.post("/api/vehicles", json=payload)

        assert response.status_code == 401


class TestVehicleList:
    def test_authenticated_user_can_list_vehicles(self, client: TestClient):
        headers = get_auth_headers(client, role=UserRole.USER)

        response = client.get("/api/vehicles", headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unauthenticated_user_cannot_list_vehicles_returns_401(self, client: TestClient):
        response = client.get("/api/vehicles")

        assert response.status_code == 401


class TestVehicleUpdate:
    def test_admin_can_update_existing_vehicle(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)
        create_payload = valid_vehicle_payload()
        create_res = client.post("/api/vehicles", json=create_payload, headers=admin_headers)
        assert create_res.status_code == 201
        vehicle_id = create_res.json()["id"]

        update_payload = valid_vehicle_payload(price=27000.0, quantity_in_stock=15)
        response = client.put(f"/api/vehicles/{vehicle_id}", json=update_payload, headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 27000.0
        assert data["quantity_in_stock"] == 15

    def test_admin_update_non_existent_vehicle_returns_404(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)
        update_payload = valid_vehicle_payload()

        response = client.put("/api/vehicles/999999", json=update_payload, headers=admin_headers)

        assert response.status_code == 404

    def test_normal_user_cannot_update_vehicle_returns_403(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)
        user_headers = get_auth_headers(client, role=UserRole.USER)

        create_res = client.post("/api/vehicles", json=valid_vehicle_payload(), headers=admin_headers)
        assert create_res.status_code == 201
        vehicle_id = create_res.json()["id"]

        update_payload = valid_vehicle_payload(price=30000.0)
        response = client.put(f"/api/vehicles/{vehicle_id}", json=update_payload, headers=user_headers)

        assert response.status_code == 403


class TestVehicleDelete:
    def test_admin_can_delete_vehicle(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)
        create_res = client.post("/api/vehicles", json=valid_vehicle_payload(), headers=admin_headers)
        assert create_res.status_code == 201
        vehicle_id = create_res.json()["id"]

        response = client.delete(f"/api/vehicles/{vehicle_id}", headers=admin_headers)

        assert response.status_code in [200, 204]

    def test_admin_delete_non_existent_vehicle_returns_404(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)

        response = client.delete("/api/vehicles/999999", headers=admin_headers)

        assert response.status_code == 404

    def test_normal_user_cannot_delete_vehicle_returns_403(self, client: TestClient):
        admin_headers = get_auth_headers(client, role=UserRole.ADMIN)
        user_headers = get_auth_headers(client, role=UserRole.USER)

        create_res = client.post("/api/vehicles", json=valid_vehicle_payload(), headers=admin_headers)
        assert create_res.status_code == 201
        vehicle_id = create_res.json()["id"]

        response = client.delete(f"/api/vehicles/{vehicle_id}", headers=user_headers)

        assert response.status_code == 403
