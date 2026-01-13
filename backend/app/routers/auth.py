"""Authentication router for user signup and signin.

This module provides endpoints for:
- POST /api/auth/signup: User registration
- POST /api/auth/signin: User login
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def signup(request: Request, user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user with email/password.

    Args:
        user_data: User registration data (email, password, username)
        session: Database session

    Returns:
        TokenResponse: JWT token and user data

    Raises:
        HTTPException 400: Email already exists or validation error
        HTTPException 500: Database error
    """
    import sys
    print(f"[DEBUG AUTH] Signup called for email: {user_data.email}", file=sys.stderr)
    print(f"[DEBUG AUTH] Session object: {session}", file=sys.stderr)
    print(f"[DEBUG AUTH] Session bind: {session.bind}", file=sys.stderr)
    print(f"[DEBUG AUTH] Session bind URL: {session.bind.url if hasattr(session.bind, 'url') else 'N/A'}", file=sys.stderr)

    try:
        # Check if email already exists (case-insensitive)
        email_lower = user_data.email.lower()
        print(f"[DEBUG AUTH] About to query for existing user...", file=sys.stderr)
        statement = select(User).where(User.email == email_lower)
        existing_user = session.exec(statement).first()
        print(f"[DEBUG AUTH] Query completed. Existing user: {existing_user is not None}", file=sys.stderr)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password with bcrypt
        hashed_password = hash_password(user_data.password)

        # Create new user
        new_user = User(
            email=email_lower,
            hashed_password=hashed_password,
            username=user_data.username,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Generate JWT token with 7-day expiration
        access_token = create_access_token(
            user_id=new_user.id,
            email=new_user.email
        )

        # Return token response with user data
        user_response = UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            is_active=new_user.is_active,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle database errors and other exceptions
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/signin", response_model=TokenResponse)
@limiter.limit("5/minute")
async def signin(request: Request, credentials: UserLogin, session: Session = Depends(get_session)):
    """Sign in an existing user with email/password.

    Args:
        credentials: Login credentials (email, password)
        session: Database session

    Returns:
        TokenResponse: JWT token and user data

    Raises:
        HTTPException 401: Invalid credentials or inactive account
        HTTPException 500: Database error
    """
    try:
        # Query user by email (case-insensitive)
        email_lower = credentials.email.lower()
        statement = select(User).where(User.email == email_lower)
        user = session.exec(statement).first()

        # Verify user exists and password is correct
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Check if user account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is inactive"
            )

        # Generate JWT token with 7-day expiration
        access_token = create_access_token(
            user_id=user.id,
            email=user.email
        )

        # Return token response with user data
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle database errors and other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sign in: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    session: Session = Depends(get_session)
):
    """Get current authenticated user information.

    This endpoint verifies the JWT token and returns the user's profile data.
    Used by the frontend to verify session validity on page load.

    Args:
        request: FastAPI request (contains user from JWT middleware)
        session: Database session

    Returns:
        UserResponse: Current user information

    Raises:
        HTTPException 401: Not authenticated (handled by middleware)
        HTTPException 404: User not found in database
        HTTPException 500: Database error
    """
    try:
        # Get user from request state (set by JWT middleware)
        if not hasattr(request.state, "user") or request.state.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_id = request.state.user["user_id"]

        # Fetch user from database
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if user account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is inactive"
            )

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle database errors and other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )
