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
    email = f"search_{role.value}_{unique}@example.com"
    password = "password123"
    username = f"search_user_{unique}"

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


def create_vehicle(client: TestClient, headers: dict, **kwargs) -> dict:
    payload = {
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 25000.0,
        "quantity_in_stock": 10,
    }
    payload.update(kwargs)
    res = client.post("/api/vehicles", json=payload, headers=headers)
    assert res.status_code == 201
    return res.json()


@pytest.fixture
def admin_headers(client: TestClient) -> dict:
    return get_auth_headers(client, role=UserRole.ADMIN)


@pytest.fixture
def user_headers(client: TestClient) -> dict:
    return get_auth_headers(client, role=UserRole.USER)


class TestSearchAuthentication:
    def test_unauthenticated_search_returns_401(self, client: TestClient):
        response = client.get("/api/vehicles/search")
        assert response.status_code == 401

    def test_authenticated_user_can_access_search(
        self, client: TestClient, user_headers: dict
    ):
        response = client.get("/api/vehicles/search", headers=user_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_authenticated_admin_can_access_search(
        self, client: TestClient, admin_headers: dict
    ):
        response = client.get("/api/vehicles/search", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestSearchNoFilters:
    def test_no_filters_returns_all_vehicles(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")
        create_vehicle(client, admin_headers, make="Ford", model="F-150", category="Truck")

        response = client.get("/api/vehicles/search", headers=user_headers)

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_no_filters_returns_empty_list_when_no_vehicles(
        self, client: TestClient, user_headers: dict
    ):
        response = client.get("/api/vehicles/search", headers=user_headers)

        assert response.status_code == 200
        assert response.json() == []


class TestSearchByMake:
    def test_search_by_make_returns_matching_vehicles(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota", model="Corolla", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"make": "Toyota"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 2
        assert all(v["make"] == "Toyota" for v in results)

    def test_search_by_make_is_case_insensitive(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"make": "toyota"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Toyota"

    def test_search_by_make_partial_match(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota Racing", model="GR86", category="Sports")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"make": "toy"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 2
        assert all("Toyota" in v["make"] for v in results)

    def test_search_by_make_no_match_returns_empty_list(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"make": "Volkswagen"}, headers=user_headers
        )

        assert response.status_code == 200
        assert response.json() == []


class TestSearchByModel:
    def test_search_by_model_returns_matching_vehicles(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"model": "Camry"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["model"] == "Camry"

    def test_search_by_model_is_case_insensitive(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"model": "camry"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["model"] == "Camry"

    def test_search_by_model_partial_match(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry SE", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota", model="Camry XSE", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"model": "cam"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 2

    def test_search_by_model_no_match_returns_empty_list(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"model": "Accord"}, headers=user_headers
        )

        assert response.status_code == 200
        assert response.json() == []


class TestSearchByCategory:
    def test_search_by_category_returns_matching_vehicles(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")
        create_vehicle(client, admin_headers, make="Ford", model="F-150", category="Truck")

        response = client.get(
            "/api/vehicles/search", params={"category": "Sedan"}, headers=user_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 2
        assert all(v["category"] == "Sedan" for v in results)

    def test_search_by_category_is_exact_match(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Ford", model="F-150", category="Truck")

        # Partial match should NOT return results for category
        response = client.get(
            "/api/vehicles/search", params={"category": "Sed"}, headers=user_headers
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_search_by_category_no_match_returns_empty_list(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")

        response = client.get(
            "/api/vehicles/search", params={"category": "SUV"}, headers=user_headers
        )

        assert response.status_code == 200
        assert response.json() == []


class TestSearchCombinedFilters:
    def test_search_by_make_and_category(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota", model="Tacoma", category="Truck")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search",
            params={"make": "Toyota", "category": "Sedan"},
            headers=user_headers,
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Toyota"
        assert results[0]["category"] == "Sedan"

    def test_search_by_make_and_model(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota", model="Corolla", category="Sedan")
        create_vehicle(client, admin_headers, make="Honda", model="Camry-lookalike", category="Sedan")

        response = client.get(
            "/api/vehicles/search",
            params={"make": "Toyota", "model": "Camry"},
            headers=user_headers,
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Toyota"
        assert results[0]["model"] == "Camry"

    def test_search_all_filters_combined(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Truck")
        create_vehicle(client, admin_headers, make="Honda", model="Civic", category="Sedan")

        response = client.get(
            "/api/vehicles/search",
            params={"make": "Toyota", "model": "Camry", "category": "Sedan"},
            headers=user_headers,
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Toyota"
        assert results[0]["model"] == "Camry"
        assert results[0]["category"] == "Sedan"

    def test_combined_filters_no_match_returns_empty_list(
        self, client: TestClient, admin_headers: dict, user_headers: dict
    ):
        create_vehicle(client, admin_headers, make="Toyota", model="Camry", category="Sedan")

        response = client.get(
            "/api/vehicles/search",
            params={"make": "Toyota", "category": "Truck"},
            headers=user_headers,
        )

        assert response.status_code == 200
        assert response.json() == []
