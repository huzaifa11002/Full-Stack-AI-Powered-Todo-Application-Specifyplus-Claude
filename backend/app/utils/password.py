"""Password hashing and verification utilities using bcrypt.

This module provides functions for:
- Hashing passwords with bcrypt (cost factor 12)
- Verifying passwords against bcrypt hashes
"""

from passlib.context import CryptContext

# Create password context with bcrypt
# Cost factor 12 provides good security/performance balance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Bcrypt has a maximum password length of 72 bytes. Passwords longer than
    72 bytes are automatically truncated to prevent errors.

    Args:
        password: Plain text password

    Returns:
        str: Bcrypt hashed password

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(hashed)
        $2b$12$...
    """
    # Bcrypt has a 72 byte limit - truncate if necessary
    # Encode to bytes, truncate, then decode back to string
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash.

    Bcrypt has a maximum password length of 72 bytes. Passwords longer than
    72 bytes are automatically truncated to match the hashing behavior.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password from database

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    # Bcrypt has a 72 byte limit - truncate if necessary to match hash_password behavior
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    return pwd_context.verify(plain_password, hashed_password)
