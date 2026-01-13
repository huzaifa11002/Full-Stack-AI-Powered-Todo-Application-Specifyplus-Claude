"""Unit tests for JWT utilities.

Tests for:
- create_access_token: JWT token creation with user_id and email
- verify_token: JWT token verification and payload extraction
"""

import pytest
import jwt as pyjwt
from datetime import datetime, timedelta
from freezegun import freeze_time

from app.utils.jwt import (
    create_access_token,
    verify_token,
    BETTER_AUTH_SECRET,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_DAYS,
)


@pytest.mark.unit
@pytest.mark.auth
class TestCreateAccessToken:
    """Test suite for create_access_token function."""

    def test_create_access_token_success(self):
        """Test successful JWT token creation with valid user data."""
        # Arrange
        user_id = 1
        email = "test@example.com"

        # Act
        token = create_access_token(user_id=user_id, email=email)

        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token can be decoded
        payload = pyjwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        assert payload["user_id"] == user_id
        assert payload["email"] == email
        assert "exp" in payload
        assert "iat" in payload

    def test_create_access_token_contains_correct_payload(self):
        """Test that token payload contains all required fields."""
        # Arrange
        user_id = 42
        email = "user@test.com"

        # Act
        token = create_access_token(user_id=user_id, email=email)
        payload = pyjwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        # Assert
        assert payload["user_id"] == user_id
        assert payload["email"] == email
        assert isinstance(payload["exp"], int)
        assert isinstance(payload["iat"], int)

    @freeze_time("2026-01-11 12:00:00")
    def test_create_access_token_expiration_time(self):
        """Test that token has correct expiration time (7 days)."""
        # Arrange
        user_id = 1
        email = "test@example.com"
        expected_exp = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

        # Act
        token = create_access_token(user_id=user_id, email=email)
        payload = pyjwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        # Assert
        exp_datetime = datetime.fromtimestamp(payload["exp"])
        assert abs((exp_datetime - expected_exp).total_seconds()) < 2  # Allow 2 second tolerance

    def test_create_access_token_with_different_users(self):
        """Test that different users get different tokens."""
        # Arrange
        user1_id = 1
        user1_email = "user1@example.com"
        user2_id = 2
        user2_email = "user2@example.com"

        # Act
        token1 = create_access_token(user_id=user1_id, email=user1_email)
        token2 = create_access_token(user_id=user2_id, email=user2_email)

        # Assert
        assert token1 != token2

        payload1 = pyjwt.decode(token1, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        payload2 = pyjwt.decode(token2, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        assert payload1["user_id"] == user1_id
        assert payload2["user_id"] == user2_id
        assert payload1["email"] == user1_email
        assert payload2["email"] == user2_email

    def test_create_access_token_with_special_characters_in_email(self):
        """Test token creation with special characters in email."""
        # Arrange
        user_id = 1
        email = "test+special@example.co.uk"

        # Act
        token = create_access_token(user_id=user_id, email=email)
        payload = pyjwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        # Assert
        assert payload["email"] == email

    def test_create_access_token_with_large_user_id(self):
        """Test token creation with large user ID."""
        # Arrange
        user_id = 999999999
        email = "test@example.com"

        # Act
        token = create_access_token(user_id=user_id, email=email)
        payload = pyjwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

        # Assert
        assert payload["user_id"] == user_id


@pytest.mark.unit
@pytest.mark.auth
class TestVerifyToken:
    """Test suite for verify_token function."""

    def test_verify_token_success(self):
        """Test successful token verification with valid token."""
        # Arrange
        user_id = 1
        email = "test@example.com"
        token = create_access_token(user_id=user_id, email=email)

        # Act
        payload = verify_token(token)

        # Assert
        assert payload is not None
        assert payload["user_id"] == user_id
        assert payload["email"] == email
        assert "exp" in payload
        assert "iat" in payload

    def test_verify_token_with_expired_token(self):
        """Test token verification fails with expired token."""
        # Arrange
        user_id = 1
        email = "test@example.com"
        expire = datetime.utcnow() - timedelta(days=1)  # Expired 1 day ago
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow() - timedelta(days=2),
        }
        expired_token = pyjwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)

        # Act & Assert
        with pytest.raises(pyjwt.ExpiredSignatureError, match="Token has expired"):
            verify_token(expired_token)

    def test_verify_token_with_invalid_signature(self):
        """Test token verification fails with invalid signature."""
        # Arrange
        user_id = 1
        email = "test@example.com"
        expire = datetime.utcnow() + timedelta(days=7)
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        # Create token with wrong secret
        invalid_token = pyjwt.encode(payload, "wrong_secret", algorithm=ALGORITHM)

        # Act & Assert
        with pytest.raises(pyjwt.InvalidTokenError, match="Invalid token"):
            verify_token(invalid_token)

    def test_verify_token_with_malformed_token(self):
        """Test token verification fails with malformed token."""
        # Arrange
        malformed_token = "not.a.valid.jwt.token"

        # Act & Assert
        with pytest.raises(pyjwt.InvalidTokenError, match="Invalid token"):
            verify_token(malformed_token)

    def test_verify_token_with_empty_token(self):
        """Test token verification fails with empty token."""
        # Arrange
        empty_token = ""

        # Act & Assert
        with pytest.raises(pyjwt.InvalidTokenError, match="Invalid token"):
            verify_token(empty_token)

    def test_verify_token_with_missing_payload_fields(self):
        """Test token verification with missing required fields still decodes."""
        # Arrange
        # Create token with minimal payload (missing user_id, email)
        expire = datetime.utcnow() + timedelta(days=7)
        payload = {
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        token = pyjwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)

        # Act
        decoded_payload = verify_token(token)

        # Assert
        # Token should decode successfully, but won't have user_id/email
        assert decoded_payload is not None
        assert "exp" in decoded_payload
        assert "iat" in decoded_payload
        assert "user_id" not in decoded_payload
        assert "email" not in decoded_payload

    def test_verify_token_with_tampered_payload(self):
        """Test token verification fails when payload is tampered."""
        # Arrange
        user_id = 1
        email = "test@example.com"
        token = create_access_token(user_id=user_id, email=email)

        # Tamper with token by modifying a character
        tampered_token = token[:-5] + "XXXXX"

        # Act & Assert
        with pytest.raises(pyjwt.InvalidTokenError, match="Invalid token"):
            verify_token(tampered_token)

    def test_verify_token_preserves_all_payload_data(self):
        """Test that verify_token returns complete payload."""
        # Arrange
        user_id = 123
        email = "complete@example.com"
        token = create_access_token(user_id=user_id, email=email)

        # Act
        payload = verify_token(token)

        # Assert
        assert len(payload) >= 4  # user_id, email, exp, iat
        assert all(key in payload for key in ["user_id", "email", "exp", "iat"])

    @freeze_time("2026-01-11 12:00:00")
    def test_verify_token_at_exact_expiration_time(self):
        """Test token verification at exact expiration boundary."""
        # Arrange
        user_id = 1
        email = "test@example.com"

        # Create token that expires in 1 second
        expire = datetime.utcnow() + timedelta(seconds=1)
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        token = pyjwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)

        # Act - verify immediately (should succeed)
        result = verify_token(token)
        assert result is not None

        # Move time forward past expiration
        with freeze_time("2026-01-11 12:00:02"):
            # Act & Assert - should fail now
            with pytest.raises(pyjwt.ExpiredSignatureError):
                verify_token(token)
