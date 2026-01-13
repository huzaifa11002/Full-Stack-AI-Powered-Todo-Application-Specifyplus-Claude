"""JWT Authentication Middleware for FastAPI.

This middleware intercepts all requests and verifies JWT tokens
for protected endpoints.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt as pyjwt

from app.utils.jwt import verify_token


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to verify JWT tokens on protected endpoints.

    Public endpoints (excluded from authentication):
    - /health, /ready
    - /docs, /openapi.json, /redoc
    - /api/auth/* (authentication endpoints)
    - / (root)
    """

    # Paths that don't require authentication
    PUBLIC_PATHS = {
        "/",
        "/health",
        "/ready",
        "/docs",
        "/openapi.json",
        "/redoc",
    }

    # Path prefixes that don't require authentication
    PUBLIC_PREFIXES = [
        "/api/auth/signup",
        "/api/auth/signin",
    ]

    async def dispatch(self, request: Request, call_next):
        """Intercept requests and verify JWT tokens for protected endpoints.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler in chain

        Returns:
            Response from next handler or 401 error
        """
        # Allow OPTIONS requests (CORS preflight) without authentication
        if request.method == "OPTIONS":
            return await call_next(request)

        # Check if path is public
        if self._is_public_path(request.url.path):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"}
            )

        # Verify Bearer token format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication credentials"}
            )

        token = parts[1]

        # Verify JWT token
        try:
            payload = verify_token(token)

            # Attach user info to request state
            request.state.user = payload

            # Continue to next handler
            return await call_next(request)

        except pyjwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has expired"}
            )
        except pyjwt.InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )
        except Exception as e:
            # Log the error internally but don't expose details to client
            import logging
            logging.error(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication failed"}
            )

    def _is_public_path(self, path: str) -> bool:
        """Check if a path is public (doesn't require authentication).

        Args:
            path: Request path

        Returns:
            True if path is public, False otherwise
        """
        # Check exact matches
        if path in self.PUBLIC_PATHS:
            return True

        # Check prefix matches
        for prefix in self.PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return True

        return False
