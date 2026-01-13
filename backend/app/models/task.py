"""Task model for todo items with user isolation.

This module defines the Task SQLModel with user_id foreign key.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    """Task model representing a todo item.

    Each task belongs to exactly one user, enforcing user isolation.
    Tasks can be created, updated, toggled, and deleted.
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, user_id={self.user_id}, title={self.title[:30]}...)"
