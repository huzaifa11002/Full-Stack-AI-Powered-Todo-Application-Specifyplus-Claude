"""Chat-related Pydantic schemas.

This module defines request/response schemas for the AI chat endpoint.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any


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
