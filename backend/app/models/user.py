"""User model for authentication and user isolation.

This module defines the User SQLModel with authentication fields.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class User(SQLModel, table=True):
    """User model representing a user in the system.

    Users own tasks and provide the foundation for user isolation.
    Includes authentication credentials (hashed_password) and account status.
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    username: str = Field(max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username}, is_active={self.is_active})"
