"""Pydantic request/response schemas for FastAPI Todo API.

This module defines:
- TaskCreate: Schema for creating new tasks
- TaskUpdate: Schema for updating existing tasks
- TaskResponse: Schema for task responses
- ChatRequest: Schema for chat message requests
- ToolCallInfo: Schema for tool call information
- ChatResponse: Schema for chat responses
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any


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


class ChatRequest(BaseModel):
    """Schema for chat message requests.

    Validates:
    - Message is not empty or whitespace-only
    - Message does not exceed 2000 characters
    - Conversation ID is optional (null for new conversations)
    """

    conversation_id: Optional[int] = Field(
        default=None, description="Optional conversation ID to continue existing conversation"
    )
    message: str = Field(
        min_length=1, max_length=2000, description="User's message to the AI assistant"
    )

    @field_validator("message")
    @classmethod
    def message_not_whitespace(cls, v: str) -> str:
        """Validate that message is not only whitespace."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or whitespace-only")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Add a task to buy groceries"
                },
                {
                    "conversation_id": 42,
                    "message": "Mark task 3 as complete"
                }
            ]
        }
    }


class ToolCallInfo(BaseModel):
    """Schema for tool call information.

    Represents a single tool invocation by the AI agent.
    """

    tool: str = Field(description="Name of the tool that was invoked")
    params: Dict[str, Any] = Field(description="Parameters passed to the tool")
    result: Any = Field(description="Result returned by the tool")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tool": "add_task",
                    "params": {"user_id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread"},
                    "result": {"id": 5, "title": "Buy groceries", "is_completed": False}
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Schema for chat responses.

    Returns conversation ID, AI response, and any tool calls made.
    """

    conversation_id: int = Field(description="ID of the conversation")
    response: str = Field(description="AI assistant's response message")
    tool_calls: List[ToolCallInfo] = Field(
        default_factory=list, description="List of tool calls made during this interaction"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": 42,
                    "response": "I've added 'Buy groceries' to your task list.",
                    "tool_calls": [
                        {
                            "tool": "add_task",
                            "params": {"user_id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread"},
                            "result": {"id": 5, "title": "Buy groceries", "is_completed": False}
                        }
                    ]
                }
            ]
        }
    }
