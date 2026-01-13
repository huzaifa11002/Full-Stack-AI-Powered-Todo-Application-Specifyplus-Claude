"""Unit tests for authentication dependencies.

Tests for:
- get_current_user: Extract authenticated user from request state
- validate_user_access: Validate user can access requested resource
"""

import pytest
from fastapi import HTTPException, Request
from unittest.mock import Mock

from app.dependencies.auth import get_current_user, validate_user_access


@pytest.mark.unit
@pytest.mark.auth
class TestGetCurrentUser:
    """Test suite for get_current_user dependency."""

    def test_get_current_user_success(self):
        """Test successful user extraction from request state."""
        # Arrange
        mock_request = Mock(spec=Request)
        user_data = {
            "user_id": 1,
            "email": "test@example.com",
            "exp": 1234567890,
            "iat": 1234567800,
        }
        mock_request.state.user = user_data

        # Act
        result = get_current_user(mock_request)

        # Assert
        assert result == user_data
        assert result["user_id"] == 1
        assert result["email"] == "test@example.com"

    def test_get_current_user_no_user_in_state(self):
        """Test that HTTPException is raised when user is not in request state."""
        # Arrange
        mock_request = Mock(spec=Request)
        mock_state = Mock(spec=[])  # Empty spec means no attributes
        mock_request.state = mock_state

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Authentication required"

    def test_get_current_user_with_none_user(self):
        """Test that HTTPException is raised when user is None."""
        # Arrange
        mock_request = Mock(spec=Request)
        mock_request.state.user = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Authentication required"

    def test_get_current_user_with_complete_user_data(self):
        """Test user extraction with all expected fields."""
        # Arrange
        mock_request = Mock(spec=Request)
        user_data = {
            "user_id": 42,
            "email": "complete@example.com",
            "exp": 1234567890,
            "iat": 1234567800,
        }
        mock_request.state.user = user_data

        # Act
        result = get_current_user(mock_request)

        # Assert
        assert "user_id" in result
        assert "email" in result
        assert "exp" in result
        assert "iat" in result
        assert result["user_id"] == 42

    def test_get_current_user_preserves_all_fields(self):
        """Test that all fields from user data are preserved."""
        # Arrange
        mock_request = Mock(spec=Request)
        user_data = {
            "user_id": 1,
            "email": "test@example.com",
            "exp": 1234567890,
            "iat": 1234567800,
            "custom_field": "custom_value",  # Extra field
        }
        mock_request.state.user = user_data

        # Act
        result = get_current_user(mock_request)

        # Assert
        assert result == user_data
        assert result["custom_field"] == "custom_value"

    def test_get_current_user_with_different_user_ids(self):
        """Test user extraction with various user IDs."""
        # Arrange
        user_ids = [1, 100, 999999, 0]

        for user_id in user_ids:
            mock_request = Mock(spec=Request)
            user_data = {
                "user_id": user_id,
                "email": f"user{user_id}@example.com",
                "exp": 1234567890,
                "iat": 1234567800,
            }
            mock_request.state.user = user_data

            # Act
            result = get_current_user(mock_request)

            # Assert
            assert result["user_id"] == user_id


@pytest.mark.unit
@pytest.mark.auth
class TestValidateUserAccess:
    """Test suite for validate_user_access function."""

    def test_validate_user_access_success(self):
        """Test successful validation when user_ids match."""
        # Arrange
        current_user = {
            "user_id": 1,
            "email": "test@example.com",
        }
        url_user_id = 1

        # Act & Assert
        # Should not raise any exception
        validate_user_access(current_user, url_user_id)

    def test_validate_user_access_mismatch_raises_403(self):
        """Test that HTTPException 403 is raised when user_ids don't match."""
        # Arrange
        current_user = {
            "user_id": 1,
            "email": "user1@example.com",
        }
        url_user_id = 2  # Different user ID

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        assert exc_info.value.status_code == 403
        assert "Access denied" in exc_info.value.detail
        assert "cannot access other users' resources" in exc_info.value.detail

    def test_validate_user_access_with_large_user_ids(self):
        """Test validation with large user IDs."""
        # Arrange
        user_id = 999999999
        current_user = {
            "user_id": user_id,
            "email": "test@example.com",
        }

        # Act & Assert
        validate_user_access(current_user, user_id)  # Should not raise

    def test_validate_user_access_prevents_user_1_accessing_user_2(self):
        """Test that user 1 cannot access user 2's resources."""
        # Arrange
        current_user = {
            "user_id": 1,
            "email": "user1@example.com",
        }
        url_user_id = 2

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        assert exc_info.value.status_code == 403

    def test_validate_user_access_prevents_user_2_accessing_user_1(self):
        """Test that user 2 cannot access user 1's resources."""
        # Arrange
        current_user = {
            "user_id": 2,
            "email": "user2@example.com",
        }
        url_user_id = 1

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        assert exc_info.value.status_code == 403

    def test_validate_user_access_with_zero_user_id(self):
        """Test validation with user_id of 0."""
        # Arrange
        current_user = {
            "user_id": 0,
            "email": "test@example.com",
        }
        url_user_id = 0

        # Act & Assert
        validate_user_access(current_user, url_user_id)  # Should not raise

    def test_validate_user_access_with_negative_user_id_mismatch(self):
        """Test validation fails with negative user ID mismatch."""
        # Arrange
        current_user = {
            "user_id": -1,
            "email": "test@example.com",
        }
        url_user_id = 1

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        assert exc_info.value.status_code == 403

    def test_validate_user_access_multiple_times_same_user(self):
        """Test that validation can be called multiple times for same user."""
        # Arrange
        current_user = {
            "user_id": 5,
            "email": "test@example.com",
        }
        url_user_id = 5

        # Act & Assert
        for _ in range(5):
            validate_user_access(current_user, url_user_id)  # Should not raise

    def test_validate_user_access_with_string_user_id_in_dict(self):
        """Test validation when user_id is stored as string (edge case)."""
        # Arrange
        # This shouldn't happen in practice, but test defensive behavior
        current_user = {
            "user_id": "1",  # String instead of int
            "email": "test@example.com",
        }
        url_user_id = 1

        # Act & Assert
        # Should raise because "1" != 1 (type mismatch)
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        assert exc_info.value.status_code == 403

    def test_validate_user_access_error_message_content(self):
        """Test that error message is informative."""
        # Arrange
        current_user = {
            "user_id": 1,
            "email": "user1@example.com",
        }
        url_user_id = 2

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        error_detail = exc_info.value.detail
        assert "Access denied" in error_detail
        assert "cannot access other users' resources" in error_detail

    def test_validate_user_access_with_missing_user_id_key(self):
        """Test validation when user_id key is missing from current_user."""
        # Arrange
        current_user = {
            "email": "test@example.com",
            # Missing user_id key
        }
        url_user_id = 1

        # Act
        # Should get None from .get() and fail validation
        with pytest.raises(HTTPException) as exc_info:
            validate_user_access(current_user, url_user_id)

        # Assert
        assert exc_info.value.status_code == 403
