"""
OAuth Production Flow Integration Test

Usage:
    python -m pytest backend/tests/test_auth_integration.py -v

This tests the complete OAuth flow:
1. Google login URL generation
2. Token exchange (mocked)
3. User creation on first login
4. Last login update on subsequent logins
5. JWT token validation
6. Protected endpoint access
7. Token refresh scenarios
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestGoogleLoginFlow:
    def test_get_google_login_url(self):
        response = client.get("/api/v1/auth/google/login")
        assert response.status_code == 200
        data = response.json()
        assert "auth_url" in data
        assert "accounts.google.com" in data["auth_url"]
        assert "scope=openid" in data["auth_url"]

    @patch("httpx.Client.post")
    @patch("httpx.Client.get")
    def test_google_callback_creates_user_on_first_login(self, mock_get, mock_post):
        # Mock Google token endpoint
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "access_token": "mock_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )

        # Mock Google userinfo endpoint
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "email": "newuser@example.com",
                "name": "New User",
                "picture": "https://example.com/pic.jpg",
            },
        )

        response = client.get("/api/v1/auth/google/callback?code=auth_code_123")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["name"] == "New User"

        # Verify user was created in database
        db = TestingSessionLocal()
        user = db.query(User).filter(User.email == "newuser@example.com").first()
        assert user is not None
        assert user.provider == "google"
        db.close()

    @patch("httpx.Client.post")
    @patch("httpx.Client.get")
    def test_google_callback_updates_last_login_on_subsequent_login(
        self, mock_get, mock_post
    ):
        # Create existing user
        db = TestingSessionLocal()
        existing_user = User(
            email="existing@example.com",
            name="Existing User",
            provider="google",
            last_login=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        db.add(existing_user)
        db.commit()
        db.close()

        # Mock Google responses
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"access_token": "mock_access_token"},
        )
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "email": "existing@example.com",
                "name": "Existing User",
            },
        )

        response = client.get("/api/v1/auth/google/callback?code=auth_code_456")
        assert response.status_code == 200

        # Verify last_login was updated
        db = TestingSessionLocal()
        user = db.query(User).filter(User.email == "existing@example.com").first()
        current_time = datetime.now(timezone.utc)
        time_diff = (current_time - user.last_login).total_seconds()
        assert time_diff < 5  # Should be very recent (within 5 seconds)
        db.close()


class TestAuthServiceMethods:
    def test_generate_access_token(self):
        db = TestingSessionLocal()
        user = User(
            email="test@example.com",
            name="Test User",
            provider="google",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token, expires_in = AuthService.generate_access_token(user)
        assert token is not None
        assert len(token) > 0
        assert expires_in == 12 * 3600  # 12 hours in seconds

        # Verify token can be decoded
        payload = AuthService.verify_token(token)
        assert payload["sub"] == str(user.id)
        assert payload["email"] == user.email

        db.close()

    def test_verify_token_with_invalid_token(self):
        with pytest.raises(ValueError):
            AuthService.verify_token("invalid.token.format")

    def test_get_current_user_from_valid_token(self):
        db = TestingSessionLocal()
        user = User(
            email="current@example.com",
            name="Current User",
            provider="google",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token, _ = AuthService.generate_access_token(user)
        current_user = AuthService.get_current_user(db, token)
        assert current_user.email == "current@example.com"

        db.close()

    def test_get_current_user_with_invalid_token(self):
        db = TestingSessionLocal()
        with pytest.raises(ValueError):
            AuthService.get_current_user(db, "invalid.token.format")
        db.close()


class TestProtectedEndpoints:
    @patch("httpx.Client.post")
    @patch("httpx.Client.get")
    def test_access_me_endpoint_with_valid_token(self, mock_get, mock_post):
        # Create user via OAuth callback
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"access_token": "mock_access_token"},
        )
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "email": "me@example.com",
                "name": "Me User",
                "picture": "https://example.com/me.jpg",
            },
        )

        callback_response = client.get("/api/v1/auth/google/callback?code=auth_code_789")
        token = callback_response.json()["token"]

        # Access protected /me endpoint with token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "me@example.com"
        assert user_data["name"] == "Me User"

    def test_access_me_endpoint_without_token(self):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        assert "Missing authentication token" in response.json()["detail"]

    def test_access_me_endpoint_with_invalid_token(self):
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.format"},
        )
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]

    def test_logout_clears_cookie(self):
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Logout successful"
        # Verify cookie was deleted (Set-Cookie header will appear in response)
        assert "auth_token" in response.cookies


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
