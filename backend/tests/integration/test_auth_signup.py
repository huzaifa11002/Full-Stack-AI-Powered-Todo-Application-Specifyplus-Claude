"""Integration tests for user signup endpoint.

Tests for POST /api/auth/signup:
- Successful user registration
- Duplicate email handling
- Invalid data validation
- Password strength requirements
- Email format validation
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import User


@pytest.mark.integration
@pytest.mark.auth
class TestSignupEndpoint:
    """Test suite for POST /api/auth/signup endpoint."""

    def test_signup_success(self, client: TestClient, session: Session):
        """Test successful user registration with valid data."""
        # Arrange
        user_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "username": "New User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == user_data["email"].lower()
        assert data["user"]["username"] == user_data["username"]
        assert data["user"]["is_active"] is True
        assert "id" in data["user"]
        assert "created_at" in data["user"]
        assert "updated_at" in data["user"]

        # Verify user was created in database
        statement = select(User).where(User.email == user_data["email"].lower())
        db_user = session.exec(statement).first()
        assert db_user is not None
        assert db_user.email == user_data["email"].lower()
        assert db_user.username == user_data["username"]

    def test_signup_duplicate_email(self, client: TestClient, test_user: User):
        """Test that signup fails with duplicate email."""
        # Arrange
        user_data = {
            "email": test_user.email,  # Use existing user's email
            "password": "SecurePass123",
            "username": "Another User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already registered" in data["detail"].lower()

    def test_signup_duplicate_email_case_insensitive(self, client: TestClient, test_user: User):
        """Test that email comparison is case-insensitive."""
        # Arrange
        user_data = {
            "email": test_user.email.upper(),  # Same email but uppercase
            "password": "SecurePass123",
            "username": "Another User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already registered" in data["detail"].lower()

    def test_signup_invalid_email_format(self, client: TestClient):
        """Test that signup fails with invalid email format."""
        # Arrange
        user_data = {
            "email": "not-an-email",
            "password": "SecurePass123",
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signup_password_too_short(self, client: TestClient):
        """Test that signup fails with password less than 8 characters."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "Short1",  # Only 6 characters
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signup_password_no_number(self, client: TestClient):
        """Test that signup fails with password without numbers."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "NoNumbersHere",
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "number" in str(data).lower()

    def test_signup_password_no_letter(self, client: TestClient):
        """Test that signup fails with password without letters."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "12345678",
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "letter" in str(data).lower()

    def test_signup_empty_username(self, client: TestClient):
        """Test that signup fails with empty username."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123",
            "username": "",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signup_whitespace_only_username(self, client: TestClient):
        """Test that signup fails with whitespace-only username."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123",
            "username": "   ",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signup_missing_required_fields(self, client: TestClient):
        """Test that signup fails with missing required fields."""
        # Arrange - missing password
        user_data = {
            "email": "test@example.com",
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signup_password_hashed_in_database(self, client: TestClient, session: Session):
        """Test that password is hashed in database, not stored as plaintext."""
        # Arrange
        user_data = {
            "email": "secure@example.com",
            "password": "PlainTextPass123",
            "username": "Secure User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201

        # Verify password is hashed
        statement = select(User).where(User.email == user_data["email"].lower())
        db_user = session.exec(statement).first()
        assert db_user is not None
        assert db_user.hashed_password != user_data["password"]
        assert db_user.hashed_password.startswith("$2b$")  # Bcrypt format

    def test_signup_email_stored_lowercase(self, client: TestClient, session: Session):
        """Test that email is stored in lowercase."""
        # Arrange
        user_data = {
            "email": "MixedCase@Example.COM",
            "password": "SecurePass123",
            "username": "Test User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == user_data["email"].lower()

        # Verify in database
        statement = select(User).where(User.email == user_data["email"].lower())
        db_user = session.exec(statement).first()
        assert db_user is not None
        assert db_user.email == user_data["email"].lower()

    def test_signup_returns_valid_jwt_token(self, client: TestClient):
        """Test that signup returns a valid JWT token."""
        # Arrange
        user_data = {
            "email": "jwt@example.com",
            "password": "SecurePass123",
            "username": "JWT User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        token = data["access_token"]

        # Verify token format (JWT has 3 parts separated by dots)
        assert token.count(".") == 2

        # Verify token can be used for authentication
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/api/1/tasks", headers=headers)
        # Should not get 401 (may get 403 if user_id mismatch, but that's OK)
        assert protected_response.status_code != 401

    def test_signup_with_special_characters_in_email(self, client: TestClient):
        """Test signup with special characters in email."""
        # Arrange
        user_data = {
            "email": "test+special@example.co.uk",
            "password": "SecurePass123",
            "username": "Special User",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == user_data["email"].lower()

    def test_signup_with_long_username(self, client: TestClient):
        """Test signup with maximum length username."""
        # Arrange
        user_data = {
            "email": "long@example.com",
            "password": "SecurePass123",
            "username": "A" * 100,  # Max length
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201

    def test_signup_username_trimmed(self, client: TestClient, session: Session):
        """Test that username whitespace is trimmed."""
        # Arrange
        user_data = {
            "email": "trim@example.com",
            "password": "SecurePass123",
            "username": "  Trimmed User  ",
        }

        # Act
        response = client.post("/api/auth/signup", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["username"] == "Trimmed User"

    def test_signup_multiple_users_sequential(self, client: TestClient):
        """Test creating multiple users sequentially."""
        # Arrange
        users = [
            {"email": f"user{i}@example.com", "password": f"Pass{i}123", "username": f"User {i}"}
            for i in range(3)
        ]

        # Act & Assert
        for user_data in users:
            response = client.post("/api/auth/signup", json=user_data)
            assert response.status_code == 201
            data = response.json()
            assert data["user"]["email"] == user_data["email"]
