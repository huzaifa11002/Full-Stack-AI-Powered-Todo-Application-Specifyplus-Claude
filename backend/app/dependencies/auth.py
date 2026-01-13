"""Authentication dependencies for FastAPI endpoints.

This module provides dependency functions for extracting
authenticated user information from requests.
"""

from fastapi import Request, HTTPException, status
from typing import Dict, Any


def get_current_user(request: Request) -> Dict[str, Any]:
    """Extract current user from request state.

    This dependency should be used in protected endpoints to get
    the authenticated user's information. The user data is set by
    the JWTAuthMiddleware after successful token verification.

    Args:
        request: FastAPI request object

    Returns:
        Dict containing user information from JWT token:
        - user_id: User's database ID
        - email: User's email address
        - exp: Token expiration timestamp
        - iat: Token issued at timestamp

    Raises:
        HTTPException 401: If user is not authenticated

    Usage:
        @app.get("/api/protected")
        def protected_endpoint(current_user: Dict = Depends(get_current_user)):
            user_id = current_user["user_id"]
            # ... use user_id
    """
    if not hasattr(request.state, "user") or request.state.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    return request.state.user


def validate_user_access(current_user: Dict[str, Any], url_user_id: int) -> None:
    """Validate that the authenticated user can access the requested resource.

    This function enforces user isolation by ensuring that the user_id
    from the JWT token matches the user_id in the URL path parameter.

    Args:
        current_user: User information from JWT token (from get_current_user)
        url_user_id: User ID from URL path parameter

    Raises:
        HTTPException 403: If user_id mismatch (user trying to access another user's resources)

    Usage:
        @app.get("/api/users/{user_id}/tasks")
        def get_tasks(
            user_id: int,
            current_user: Dict = Depends(get_current_user)
        ):
            validate_user_access(current_user, user_id)
            # ... proceed with request
    """
    token_user_id = current_user.get("user_id")

    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' resources"
        )

