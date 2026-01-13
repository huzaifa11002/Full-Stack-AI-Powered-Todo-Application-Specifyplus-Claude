"""Pydantic schemas for user authentication and responses.

This module defines:
- UserCreate: Schema for user registration
- UserLogin: Schema for user login
- UserResponse: Schema for user data responses
- TokenResponse: Schema for JWT token responses
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user (registration).

    Validates:
    - Email is valid format
    - Password meets minimum requirements (8+ chars, at least one number and letter)
    - Username is not empty
    """

    email: EmailStr = Field(description="User email address")
    password: str = Field(min_length=8, max_length=100, description="User password")
    username: str = Field(min_length=1, max_length=100, description="User display name")

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password has at least one number and one letter."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v

    @field_validator("username")
    @classmethod
    def username_not_whitespace(cls, v: str) -> str:
        """Validate that username is not only whitespace."""
        if not v or not v.strip():
            raise ValueError("Username cannot be empty or whitespace-only")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "password123",
                    "username": "John Doe",
                }
            ]
        }
    }


class UserLogin(BaseModel):
    """Schema for user login (signin).

    Validates:
    - Email is valid format
    - Password is provided
    """

    email: EmailStr = Field(description="User email address")
    password: str = Field(min_length=1, description="User password")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "password123",
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """Schema for user data responses.

    Returns user information without sensitive fields (no hashed_password).
    """

    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Enable ORM mode for SQLModel compatibility
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "John Doe",
                    "is_active": True,
                    "created_at": "2026-01-10T10:00:00Z",
                    "updated_at": "2026-01-10T10:00:00Z",
                }
            ]
        },
    }


class TokenResponse(BaseModel):
    """Schema for JWT token responses.

    Returns access token with metadata and user information.
    """

    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    user: UserResponse = Field(description="User information")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "John Doe",
                        "is_active": True,
                        "created_at": "2026-01-10T10:00:00Z",
                        "updated_at": "2026-01-10T10:00:00Z",
                    },
                }
            ]
        }
    }
