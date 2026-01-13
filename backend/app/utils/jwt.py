"""JWT token creation and verification utilities.

This module provides functions for:
- Creating JWT access tokens with user_id and expiration
- Verifying JWT tokens and extracting payload
"""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get JWT secret from environment
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError(
        "BETTER_AUTH_SECRET environment variable is not set. "
        "Please add it to your .env file."
    )

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: int, email: str) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        str: Encoded JWT token

    Token payload includes:
        - user_id: User's database ID
        - email: User's email address
        - exp: Expiration timestamp (7 days from now)
        - iat: Issued at timestamp
    """
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a JWT token and extract its payload.

    Args:
        token: JWT token string

    Returns:
        Dict[str, Any]: Decoded token payload if valid, None if invalid

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is malformed or signature is invalid
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")
