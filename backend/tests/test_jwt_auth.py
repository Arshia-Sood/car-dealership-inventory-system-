from datetime import datetime, timedelta, timezone
import uuid

import jwt
import pytest
from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.database import SessionLocal
from app.main import app
from app.models.user import User, UserRole

# Try importing dependencies that will be implemented in the GREEN phase.
# If they don't exist yet, fallback to dummy dependencies so pytest can collect tests.
try:
    from app.api.deps import get_current_user, require_admin
except ImportError:
    from fastapi import HTTPException, status

    def get_current_user():
        """Placeholder dependency for RED phase - fails until implemented."""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="get_current_user dependency not implemented yet",
        )

    def require_admin():
        """Placeholder dependency for RED phase - fails until implemented."""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="require_admin dependency not implemented yet",
        )



# Register temporary protected endpoints for JWT auth testing
test_router = APIRouter(prefix="/api/test", tags=["test"])


@test_router.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"message": "protected content"}


@test_router.get("/admin-only")
def admin_only_route(current_user=Depends(require_admin)):
    return {"message": "admin content"}


app.include_router(test_router)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def create_user_in_db(role: UserRole = UserRole.USER) -> dict:
    """Helper to create a user directly in DB with specified role and return credentials."""
    unique = uuid.uuid4().hex[:8]
    email = f"jwt_{role.value}_{unique}@example.com"
    password = "password123"
    username = f"user_{unique}"

    # Register via client to ensure standard hashing and setup
    with TestClient(app) as test_client:
        res = test_client.post(
            "/api/auth/register",
            json={"email": email, "username": username, "password": password},
        )
        assert res.status_code == 201

    if role == UserRole.ADMIN:
        with SessionLocal() as session:
            user = session.query(User).filter(User.email == email).first()
            user.role = UserRole.ADMIN
            session.commit()

    return {"email": email, "password": password, "role": role.value}


def get_token_for_user(client: TestClient, credentials: dict) -> str:
    """Helper to perform login and retrieve access token."""
    res = client.post(
        "/api/auth/login",
        json={"email": credentials["email"], "password": credentials["password"]},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


class TestProtectedRoutesJWTAuth:
    def test_access_protected_endpoint_without_jwt_returns_401(self, client: TestClient):
        response = client.get("/api/test/protected")
        assert response.status_code == 401

    def test_access_protected_endpoint_with_invalid_jwt_returns_401(self, client: TestClient):
        headers = {"Authorization": "Bearer invalid.jwt.token"}
        response = client.get("/api/test/protected", headers=headers)
        assert response.status_code == 401

    def test_access_protected_endpoint_with_expired_jwt_returns_401(self, client: TestClient):
        expired_payload = {
            "sub": "1",
            "email": "user@example.com",
            "role": "user",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=10),
        }
        expired_token = jwt.encode(
            expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/test/protected", headers=headers)
        assert response.status_code == 401


class TestAdminOnlyRoutesAuth:
    def test_access_admin_endpoint_with_normal_user_jwt_returns_403(self, client: TestClient):
        user_credentials = create_user_in_db(role=UserRole.USER)
        user_token = get_token_for_user(client, user_credentials)
        headers = {"Authorization": f"Bearer {user_token}"}

        response = client.get("/api/test/admin-only", headers=headers)
        assert response.status_code == 403

    def test_access_admin_endpoint_with_admin_jwt_succeeds(self, client: TestClient):
        admin_credentials = create_user_in_db(role=UserRole.ADMIN)
        admin_token = get_token_for_user(client, admin_credentials)
        headers = {"Authorization": f"Bearer {admin_token}"}

        response = client.get("/api/test/admin-only", headers=headers)
        assert response.status_code == 200
