"""Integration tests for JWT middleware and protected endpoints.

Tests for:
- JWT middleware authentication
- Protected endpoint access with valid/invalid tokens
- Token expiration handling
- Authorization header validation
- Public vs protected endpoint routing
"""

import pytest
from fastapi.testclient import TestClient

from app.models import User, Task


@pytest.mark.integration
@pytest.mark.auth
class TestJWTMiddleware:
    """Test suite for JWT authentication middleware."""

    def test_protected_endpoint_without_token(self, client: TestClient, test_user: User):
        """Test that protected endpoint requires authentication."""
        # Act
        response = client.get(f"/api/{test_user.id}/tasks")

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "authentication required" in data["detail"].lower()

    def test_protected_endpoint_with_valid_token(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test that protected endpoint accepts valid JWT token."""
        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)

        # Assert
        assert response.status_code == 200  # Authenticated successfully

    def test_protected_endpoint_with_invalid_token(self, client: TestClient, test_user: User):
        """Test that protected endpoint rejects invalid token."""
        # Arrange
        headers = {"Authorization": "Bearer invalid.jwt.token"}

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "invalid token" in data["detail"].lower()

    def test_protected_endpoint_with_expired_token(
        self, client: TestClient, test_user: User, expired_token: str
    ):
        """Test that protected endpoint rejects expired token."""
        # Arrange
        headers = {"Authorization": f"Bearer {expired_token}"}

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "expired" in data["detail"].lower()

    def test_protected_endpoint_with_malformed_authorization_header(
        self, client: TestClient, test_user: User, auth_token: str
    ):
        """Test that malformed Authorization header is rejected."""
        # Arrange - Missing "Bearer" prefix
        headers = {"Authorization": auth_token}

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        assert response.status_code == 401

    def test_protected_endpoint_with_wrong_token_type(
        self, client: TestClient, test_user: User, auth_token: str
    ):
        """Test that wrong token type (not Bearer) is rejected."""
        # Arrange
        headers = {"Authorization": f"Basic {auth_token}"}

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        assert response.status_code == 401

    def test_protected_endpoint_with_empty_authorization_header(
        self, client: TestClient, test_user: User
    ):
        """Test that empty Authorization header is rejected."""
        # Arrange
        headers = {"Authorization": ""}

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        assert response.status_code == 401

    def test_public_endpoint_without_token(self, client: TestClient):
        """Test that public endpoints don't require authentication."""
        # Act
        response = client.get("/health")

        # Assert
        # Should succeed without authentication (or 404 if endpoint doesn't exist)
        assert response.status_code in [200, 404]

    def test_auth_endpoints_are_public(self, client: TestClient):
        """Test that auth endpoints don't require authentication."""
        # Arrange
        signup_data = {
            "email": "public@example.com",
            "password": "PublicPass123",
            "username": "Public User",
        }

        # Act - Should work without Authorization header
        response = client.post("/api/auth/signup", json=signup_data)

        # Assert
        assert response.status_code == 201

    def test_docs_endpoint_is_public(self, client: TestClient):
        """Test that documentation endpoints are public."""
        # Act
        response = client.get("/docs")

        # Assert
        # Should succeed or redirect without authentication
        assert response.status_code in [200, 307]

    def test_openapi_endpoint_is_public(self, client: TestClient):
        """Test that OpenAPI schema endpoint is public."""
        # Act
        response = client.get("/openapi.json")

        # Assert
        assert response.status_code == 200

    def test_multiple_requests_with_same_token(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test that same token can be used for multiple requests."""
        # Act - Make 3 requests with same token
        responses = [
            client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)
            for _ in range(3)
        ]

        # Assert - All should succeed
        assert all(r.status_code == 200 for r in responses)

    def test_different_tokens_for_different_users(
        self,
        client: TestClient,
        test_user: User,
        test_user_2: User,
        auth_headers: dict,
        auth_headers_2: dict,
    ):
        """Test that different users have different tokens."""
        # Act
        response_1 = client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)
        response_2 = client.get(f"/api/{test_user_2.id}/tasks", headers=auth_headers_2)

        # Assert
        assert response_1.status_code == 200
        assert response_2.status_code == 200

    def test_token_from_user_1_cannot_access_user_2_resources(
        self, client: TestClient, test_user: User, test_user_2: User, auth_headers: dict
    ):
        """Test user isolation - User 1's token cannot access User 2's resources."""
        # Act - Try to access user 2's tasks with user 1's token
        response = client.get(f"/api/{test_user_2.id}/tasks", headers=auth_headers)

        # Assert
        assert response.status_code == 403  # Forbidden
        data = response.json()
        assert "access denied" in data["detail"].lower()

    def test_create_task_requires_authentication(
        self, client: TestClient, test_user: User, task_data: dict
    ):
        """Test that creating a task requires authentication."""
        # Act
        response = client.post(f"/api/{test_user.id}/tasks", json=task_data)

        # Assert
        assert response.status_code == 401

    def test_create_task_with_valid_token(
        self, client: TestClient, test_user: User, auth_headers: dict, task_data: dict
    ):
        """Test that creating a task works with valid token."""
        # Act
        response = client.post(
            f"/api/{test_user.id}/tasks", json=task_data, headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == test_user.id
        assert data["title"] == task_data["title"]

    def test_update_task_requires_authentication(
        self, client: TestClient, test_user: User, test_task: Task
    ):
        """Test that updating a task requires authentication."""
        # Arrange
        update_data = {"title": "Updated Title"}

        # Act
        response = client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}", json=update_data
        )

        # Assert
        assert response.status_code == 401

    def test_delete_task_requires_authentication(
        self, client: TestClient, test_user: User, test_task: Task
    ):
        """Test that deleting a task requires authentication."""
        # Act
        response = client.delete(f"/api/{test_user.id}/tasks/{test_task.id}")

        # Assert
        assert response.status_code == 401

    def test_toggle_task_requires_authentication(
        self, client: TestClient, test_user: User, test_task: Task
    ):
        """Test that toggling a task requires authentication."""
        # Act
        response = client.patch(f"/api/{test_user.id}/tasks/{test_task.id}/toggle")

        # Assert
        assert response.status_code == 401

    def test_get_task_requires_authentication(
        self, client: TestClient, test_user: User, test_task: Task
    ):
        """Test that getting a task requires authentication."""
        # Act
        response = client.get(f"/api/{test_user.id}/tasks/{test_task.id}")

        # Assert
        assert response.status_code == 401

    def test_authorization_header_case_insensitive_bearer(
        self, client: TestClient, test_user: User, auth_token: str
    ):
        """Test that 'Bearer' is case-insensitive in Authorization header."""
        # Arrange
        headers_lowercase = {"Authorization": f"bearer {auth_token}"}
        headers_uppercase = {"Authorization": f"BEARER {auth_token}"}
        headers_mixed = {"Authorization": f"BeArEr {auth_token}"}

        # Act
        response_lowercase = client.get(
            f"/api/{test_user.id}/tasks", headers=headers_lowercase
        )
        response_uppercase = client.get(
            f"/api/{test_user.id}/tasks", headers=headers_uppercase
        )
        response_mixed = client.get(f"/api/{test_user.id}/tasks", headers=headers_mixed)

        # Assert - All should work
        assert response_lowercase.status_code == 200
        assert response_uppercase.status_code == 200
        assert response_mixed.status_code == 200

    def test_token_with_extra_whitespace(
        self, client: TestClient, test_user: User, auth_token: str
    ):
        """Test that extra whitespace in Authorization header is handled."""
        # Arrange
        headers = {"Authorization": f"Bearer  {auth_token}"}  # Extra space

        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=headers)

        # Assert
        # Should fail because of extra space
        assert response.status_code == 401

    def test_middleware_attaches_user_to_request_state(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test that middleware attaches user info to request state."""
        # Act
        response = client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)

        # Assert
        # If middleware works correctly, endpoint should have access to user info
        assert response.status_code == 200

    def test_concurrent_requests_with_different_tokens(
        self,
        client: TestClient,
        test_user: User,
        test_user_2: User,
        auth_headers: dict,
        auth_headers_2: dict,
    ):
        """Test that concurrent requests with different tokens work correctly."""
        # Act - Simulate concurrent requests
        response_1a = client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)
        response_2a = client.get(f"/api/{test_user_2.id}/tasks", headers=auth_headers_2)
        response_1b = client.get(f"/api/{test_user.id}/tasks", headers=auth_headers)
        response_2b = client.get(f"/api/{test_user_2.id}/tasks", headers=auth_headers_2)

        # Assert - All should succeed
        assert response_1a.status_code == 200
        assert response_2a.status_code == 200
        assert response_1b.status_code == 200
        assert response_2b.status_code == 200
