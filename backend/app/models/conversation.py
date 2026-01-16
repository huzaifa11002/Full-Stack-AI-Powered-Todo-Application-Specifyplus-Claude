"""Conversation model for AI chat sessions.

This module defines the Conversation SQLModel for storing chat sessions.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Conversation(SQLModel, table=True):
    """Conversation model representing a chat session.

    A conversation represents a continuous chat session between a user
    and the AI assistant. All messages within a conversation share context.
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, user_id={self.user_id}, created_at={self.created_at})"
