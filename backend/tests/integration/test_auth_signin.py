"""Integration tests for user signin endpoint.

Tests for POST /api/auth/signin:
- Successful user login
- Invalid credentials handling
- Inactive account handling
- Case-insensitive email matching
- JWT token generation
"""

import pytest
from fastapi.testclient import TestClient

from app.models import User


@pytest.mark.integration
@pytest.mark.auth
class TestSigninEndpoint:
    """Test suite for POST /api/auth/signin endpoint."""

    def test_signin_success(self, client: TestClient, test_user: User):
        """Test successful user login with valid credentials."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "TestPass123",  # From fixture
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user.email
        assert data["user"]["username"] == test_user.username
        assert data["user"]["is_active"] is True
        assert data["user"]["id"] == test_user.id

    def test_signin_wrong_password(self, client: TestClient, test_user: User):
        """Test that signin fails with incorrect password."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "WrongPassword123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid credentials" in data["detail"].lower()

    def test_signin_nonexistent_email(self, client: TestClient):
        """Test that signin fails with non-existent email."""
        # Arrange
        credentials = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "invalid credentials" in data["detail"].lower()

    def test_signin_inactive_account(self, client: TestClient, inactive_user: User):
        """Test that signin fails for inactive account."""
        # Arrange
        credentials = {
            "email": inactive_user.email,
            "password": "TestPass789",  # From fixture
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "inactive" in data["detail"].lower()

    def test_signin_case_insensitive_email(self, client: TestClient, test_user: User):
        """Test that email matching is case-insensitive."""
        # Arrange
        credentials = {
            "email": test_user.email.upper(),  # Uppercase email
            "password": "TestPass123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == test_user.email.lower()

    def test_signin_mixed_case_email(self, client: TestClient, test_user: User):
        """Test signin with mixed case email."""
        # Arrange
        # Create email with mixed case from stored lowercase
        mixed_case_email = test_user.email[:3].upper() + test_user.email[3:]
        credentials = {
            "email": mixed_case_email,
            "password": "TestPass123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200

    def test_signin_invalid_email_format(self, client: TestClient):
        """Test that signin fails with invalid email format."""
        # Arrange
        credentials = {
            "email": "not-an-email",
            "password": "SomePassword123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signin_empty_password(self, client: TestClient, test_user: User):
        """Test that signin fails with empty password."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signin_missing_email(self, client: TestClient):
        """Test that signin fails with missing email."""
        # Arrange
        credentials = {
            "password": "SomePassword123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signin_missing_password(self, client: TestClient, test_user: User):
        """Test that signin fails with missing password."""
        # Arrange
        credentials = {
            "email": test_user.email,
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_signin_returns_valid_jwt_token(self, client: TestClient, test_user: User):
        """Test that signin returns a valid JWT token."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "TestPass123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        token = data["access_token"]

        # Verify token format (JWT has 3 parts separated by dots)
        assert token.count(".") == 2

        # Verify token can be used for authentication
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get(f"/api/{test_user.id}/tasks", headers=headers)
        # Should not get 401 (authenticated successfully)
        assert protected_response.status_code != 401

    def test_signin_token_contains_user_info(self, client: TestClient, test_user: User):
        """Test that JWT token contains correct user information."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "TestPass123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        token = data["access_token"]

        # Decode token to verify payload
        import jwt
        from app.utils.jwt import BETTER_AUTH_SECRET, ALGORITHM
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        assert payload["user_id"] == test_user.id
        assert payload["email"] == test_user.email
        assert "exp" in payload
        assert "iat" in payload

    def test_signin_password_case_sensitive(self, client: TestClient, test_user: User):
        """Test that password matching is case-sensitive."""
        # Arrange
        credentials_lowercase = {
            "email": test_user.email,
            "password": "testpass123",  # Wrong case
        }
        credentials_uppercase = {
            "email": test_user.email,
            "password": "TESTPASS123",  # Wrong case
        }

        # Act
        response_lowercase = client.post("/api/auth/signin", json=credentials_lowercase)
        response_uppercase = client.post("/api/auth/signin", json=credentials_uppercase)

        # Assert
        assert response_lowercase.status_code == 401
        assert response_uppercase.status_code == 401

    def test_signin_multiple_times_same_user(self, client: TestClient, test_user: User):
        """Test that user can sign in multiple times."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "TestPass123",
        }

        # Act - Sign in 3 times
        tokens = []
        for _ in range(3):
            response = client.post("/api/auth/signin", json=credentials)
            assert response.status_code == 200
            tokens.append(response.json()["access_token"])

        # Assert - All tokens should be different (different iat timestamps)
        assert len(set(tokens)) == 3

    def test_signin_different_users(self, client: TestClient, test_user: User, test_user_2: User):
        """Test signin for different users."""
        # Arrange
        credentials_1 = {
            "email": test_user.email,
            "password": "TestPass123",
        }
        credentials_2 = {
            "email": test_user_2.email,
            "password": "TestPass456",
        }

        # Act
        response_1 = client.post("/api/auth/signin", json=credentials_1)
        response_2 = client.post("/api/auth/signin", json=credentials_2)

        # Assert
        assert response_1.status_code == 200
        assert response_2.status_code == 200

        data_1 = response_1.json()
        data_2 = response_2.json()

        assert data_1["user"]["id"] == test_user.id
        assert data_2["user"]["id"] == test_user_2.id
        assert data_1["access_token"] != data_2["access_token"]

    def test_signin_with_whitespace_in_password(self, client: TestClient, test_user: User):
        """Test that whitespace in password is significant."""
        # Arrange
        credentials_with_space = {
            "email": test_user.email,
            "password": "TestPass123 ",  # Extra space
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials_with_space)

        # Assert
        assert response.status_code == 401  # Should fail

    def test_signin_error_message_does_not_leak_info(self, client: TestClient, test_user: User):
        """Test that error messages don't reveal whether email exists."""
        # Arrange
        wrong_email = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123",
        }
        wrong_password = {
            "email": test_user.email,
            "password": "WrongPassword123",
        }

        # Act
        response_wrong_email = client.post("/api/auth/signin", json=wrong_email)
        response_wrong_password = client.post("/api/auth/signin", json=wrong_password)

        # Assert - Both should return same generic error
        assert response_wrong_email.status_code == 401
        assert response_wrong_password.status_code == 401
        assert response_wrong_email.json()["detail"] == response_wrong_password.json()["detail"]
        assert "invalid credentials" in response_wrong_email.json()["detail"].lower()

    def test_signin_does_not_return_password(self, client: TestClient, test_user: User):
        """Test that response does not contain password or hashed_password."""
        # Arrange
        credentials = {
            "email": test_user.email,
            "password": "TestPass123",
        }

        # Act
        response = client.post("/api/auth/signin", json=credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        response_str = str(data).lower()

        # Verify no password fields in response
        assert "password" not in response_str
        assert "hashed_password" not in response_str
        assert "$2b$" not in response_str  # Bcrypt hash format
