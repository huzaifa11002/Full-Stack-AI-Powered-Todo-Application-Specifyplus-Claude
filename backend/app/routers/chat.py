"""Chat router for AI-powered task management conversations.

This module implements the chat endpoint that enables users to interact
with the AI assistant for task management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import json
import logging
from datetime import datetime

from app.database import get_session
from app.models import Conversation, Message, User
from app.schemas import ChatRequest, ChatResponse, ToolCallInfo
from app.dependencies.auth import get_current_user
from chat_agents.runner import run_agent_conversation

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def get_or_create_conversation(
    session: Session,
    user_id: int,
    conversation_id: int | None
) -> Conversation:
    """Get existing conversation or create a new one.

    Args:
        session: Database session
        user_id: ID of the user
        conversation_id: Optional conversation ID to continue

    Returns:
        Conversation object

    Raises:
        HTTPException: If conversation doesn't exist or doesn't belong to user
    """
    if conversation_id:
        # Get existing conversation
        conversation = session.get(Conversation, conversation_id)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found"
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conversation does not belong to user"
            )

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        return conversation
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation


def get_conversation_history(
    session: Session,
    conversation_id: int
) -> List[dict]:
    """Fetch conversation history ordered by creation time.

    Args:
        session: Database session
        conversation_id: ID of the conversation

    Returns:
        List of message dictionaries with role and content
    """
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    messages = session.exec(statement).all()

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]


def store_messages(
    session: Session,
    conversation_id: int,
    user_id: int,
    user_message: str,
    assistant_response: str,
    tool_calls: List[dict]
) -> None:
    """Store user and assistant messages in the database.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user
        user_message: User's message content
        assistant_response: Assistant's response content
        tool_calls: List of tool calls made (for logging)
    """
    # Store user message
    user_msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=user_message,
        tool_calls=None,
        created_at=datetime.utcnow()
    )
    session.add(user_msg)

    # Store assistant message with tool calls
    tool_calls_json = json.dumps(tool_calls) if tool_calls else None
    assistant_msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=assistant_response,
        tool_calls=tool_calls_json,
        created_at=datetime.utcnow()
    )
    session.add(assistant_msg)

    session.commit()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """Send message to AI chat assistant.

    This endpoint enables users to interact with the AI assistant for task management.
    The assistant interprets natural language, invokes appropriate tools, and returns
    conversational responses.

    Args:
        user_id: ID of the user (must match authenticated user)
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user from JWT token (dict)
        session: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool_calls

    Raises:
        HTTPException: If user_id doesn't match authenticated user or other errors
    """
    # Verify user_id matches authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID does not match authenticated user"
        )

    try:
        # Get or create conversation
        conversation = get_or_create_conversation(
            session, user_id, request.conversation_id
        )

        # Get conversation history
        history = get_conversation_history(session, conversation.id)

        # Run agent conversation
        logger.info(f"Processing chat message for user {user_id}, conversation {conversation.id}")
        assistant_response, tool_calls = await run_agent_conversation(
            user_id=user_id,
            messages=history,
            new_message=request.message
        )

        # Store messages
        store_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            user_message=request.message,
            assistant_response=assistant_response,
            tool_calls=tool_calls
        )

        # Convert tool calls to response format
        tool_call_infos = [
            ToolCallInfo(
                tool=tc["tool"],
                params=tc["params"],
                result=tc["result"]
            )
            for tc in tool_calls
        ]

        logger.info(f"Chat response generated for user {user_id}, {len(tool_calls)} tool calls")

        return ChatResponse(
            conversation_id=conversation.id,
            response=assistant_response,
            tool_calls=tool_call_infos
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )
