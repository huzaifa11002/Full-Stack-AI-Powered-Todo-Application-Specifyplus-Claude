"""Unit tests for password utilities.

Tests for:
- hash_password: Password hashing with bcrypt
- verify_password: Password verification against bcrypt hash
"""

import pytest
from app.utils.password import hash_password, verify_password


@pytest.mark.unit
@pytest.mark.auth
class TestHashPassword:
    """Test suite for hash_password function."""

    def test_hash_password_success(self):
        """Test successful password hashing."""
        # Arrange
        password = "MySecurePassword123"

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password  # Hash should be different from plain password
        assert hashed.startswith("$2b$")  # Bcrypt hash format

    def test_hash_password_different_hashes_for_same_password(self):
        """Test that same password produces different hashes (salt)."""
        # Arrange
        password = "SamePassword123"

        # Act
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Assert
        assert hash1 != hash2  # Different salts should produce different hashes
        assert hash1.startswith("$2b$")
        assert hash2.startswith("$2b$")

    def test_hash_password_with_special_characters(self):
        """Test password hashing with special characters."""
        # Arrange
        password = "P@ssw0rd!#$%^&*()"

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_unicode_characters(self):
        """Test password hashing with unicode characters."""
        # Arrange
        password = "Пароль123"  # Russian characters

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_long_password(self):
        """Test password hashing with very long password."""
        # Arrange
        password = "a" * 100  # 100 character password

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_short_password(self):
        """Test password hashing with short password."""
        # Arrange
        password = "abc"

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_empty_string(self):
        """Test password hashing with empty string."""
        # Arrange
        password = ""

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_with_whitespace(self):
        """Test password hashing with whitespace."""
        # Arrange
        password = "   password with spaces   "

        # Act
        hashed = hash_password(password)

        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")


@pytest.mark.unit
@pytest.mark.auth
class TestVerifyPassword:
    """Test suite for verify_password function."""

    def test_verify_password_success(self):
        """Test successful password verification with correct password."""
        # Arrange
        password = "CorrectPassword123"
        hashed = hash_password(password)

        # Act
        result = verify_password(password, hashed)

        # Assert
        assert result is True

    def test_verify_password_failure_wrong_password(self):
        """Test password verification fails with wrong password."""
        # Arrange
        correct_password = "CorrectPassword123"
        wrong_password = "WrongPassword456"
        hashed = hash_password(correct_password)

        # Act
        result = verify_password(wrong_password, hashed)

        # Assert
        assert result is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        # Arrange
        password = "Password123"
        hashed = hash_password(password)

        # Act
        result_lowercase = verify_password("password123", hashed)
        result_uppercase = verify_password("PASSWORD123", hashed)
        result_correct = verify_password("Password123", hashed)

        # Assert
        assert result_lowercase is False
        assert result_uppercase is False
        assert result_correct is True

    def test_verify_password_with_special_characters(self):
        """Test password verification with special characters."""
        # Arrange
        password = "P@ssw0rd!#$%"
        hashed = hash_password(password)

        # Act
        result = verify_password(password, hashed)

        # Assert
        assert result is True

    def test_verify_password_with_unicode_characters(self):
        """Test password verification with unicode characters."""
        # Arrange
        password = "Пароль123"
        hashed = hash_password(password)

        # Act
        result = verify_password(password, hashed)

        # Assert
        assert result is True

    def test_verify_password_with_whitespace_preserved(self):
        """Test that whitespace in password is preserved."""
        # Arrange
        password_with_spaces = "   password   "
        password_without_spaces = "password"
        hashed = hash_password(password_with_spaces)

        # Act
        result_with_spaces = verify_password(password_with_spaces, hashed)
        result_without_spaces = verify_password(password_without_spaces, hashed)

        # Assert
        assert result_with_spaces is True
        assert result_without_spaces is False

    def test_verify_password_with_empty_password(self):
        """Test password verification with empty password."""
        # Arrange
        password = ""
        hashed = hash_password(password)

        # Act
        result_correct = verify_password("", hashed)
        result_wrong = verify_password("something", hashed)

        # Assert
        assert result_correct is True
        assert result_wrong is False

    def test_verify_password_with_similar_passwords(self):
        """Test that similar passwords don't match."""
        # Arrange
        password1 = "Password123"
        password2 = "Password124"  # Only last digit different
        hashed = hash_password(password1)

        # Act
        result1 = verify_password(password1, hashed)
        result2 = verify_password(password2, hashed)

        # Assert
        assert result1 is True
        assert result2 is False

    def test_verify_password_with_invalid_hash(self):
        """Test password verification with invalid hash format."""
        # Arrange
        password = "Password123"
        invalid_hash = "not_a_valid_bcrypt_hash"

        # Act & Assert
        # Should raise an exception or return False
        with pytest.raises(Exception):
            verify_password(password, invalid_hash)

    def test_verify_password_multiple_times_same_result(self):
        """Test that verifying same password multiple times gives consistent results."""
        # Arrange
        password = "ConsistentPassword123"
        hashed = hash_password(password)

        # Act
        results = [verify_password(password, hashed) for _ in range(5)]

        # Assert
        assert all(result is True for result in results)

    def test_verify_password_with_long_password(self):
        """Test password verification with very long password.

        Note: Bcrypt truncates passwords to 72 bytes, so passwords longer than
        72 bytes that share the same first 72 bytes will match. This is a known
        limitation of bcrypt.
        """
        # Arrange
        password = "a" * 100
        hashed = hash_password(password)

        # Act
        result_correct = verify_password(password, hashed)
        # Both passwords get truncated to 72 bytes, so they match
        result_wrong = verify_password("a" * 99, hashed)

        # Assert
        assert result_correct is True
        # Due to bcrypt's 72-byte truncation, this also matches
        assert result_wrong is True

    def test_hash_and_verify_integration(self):
        """Integration test for hash and verify workflow."""
        # Arrange
        passwords = [
            "SimplePassword123",
            "Complex!@#$%^&*()Password",
            "Пароль123",
            "   spaces   ",
            "a" * 72,  # Bcrypt max length
        ]

        for password in passwords:
            # Act
            hashed = hash_password(password)
            result = verify_password(password, hashed)

            # Assert
            assert result is True, f"Failed for password: {password}"
