"""Message model for conversation messages.

This module defines the Message SQLModel for storing individual messages.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import field_validator

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Message model representing a single message in a conversation.

    Messages can be from the user or the AI assistant. Each message
    belongs to exactly one conversation and one user.
    """

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=20)
    content: str = Field(min_length=1)
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate that role is either 'user' or 'assistant'."""
        if v not in ("user", "assistant"):
            raise ValueError("role must be 'user' or 'assistant'")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate that content is not empty."""
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        return v

    def __repr__(self) -> str:
        return f"Message(id={self.id}, conversation_id={self.conversation_id}, role={self.role})"
