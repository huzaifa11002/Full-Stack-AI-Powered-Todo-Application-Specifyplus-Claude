"""Pydantic request/response schemas for FastAPI Todo API.

This module defines:
- TaskCreate: Schema for creating new tasks
- TaskUpdate: Schema for updating existing tasks
- TaskResponse: Schema for task responses
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Validates:
    - Title is not empty or whitespace-only
    - Title does not exceed 200 characters
    - Description does not exceed 2000 characters if provided
    """

    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Optional task description"
    )

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: str) -> str:
        """Validate that title is not only whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread, and vegetables",
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.
    """

    title: Optional[str] = Field(
        default=None, max_length=200, description="Updated task title"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Updated task description"
    )
    is_completed: Optional[bool] = Field(
        default=None, description="Updated completion status"
    )

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not only whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip() if v else None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and cook dinner",
                    "description": "Updated shopping list",
                    "is_completed": True,
                }
            ]
        }
    }


class TaskResponse(BaseModel):
    """Schema for task responses.

    Returns all task fields including timestamps.
    """

    id: int
    user_id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Enable ORM mode for SQLModel compatibility
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread, and vegetables",
                    "is_completed": False,
                    "created_at": "2026-01-10T10:00:00Z",
                    "updated_at": "2026-01-10T10:00:00Z",
                }
            ]
        },
    }
