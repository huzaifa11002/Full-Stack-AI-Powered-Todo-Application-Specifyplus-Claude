"""Agent creation and function tools for OpenAI Agents SDK.

This module provides function tools decorated with @function_tool
for use with the OpenAI Agents SDK.
"""

from typing import Dict, Any, Optional
from agents import Agent, function_tool
from mcp_tools.server import mcp_server
from .gemini_config import model, SYSTEM_PROMPT


# Context variable to store current user_id (injected by runner)
_current_user_id: Optional[int] = None


def set_user_context(user_id: Optional[int]):
    """Set the current user ID in context."""
    global _current_user_id
    _current_user_id = user_id


def get_user_context() -> int:
    """Get the current user ID from context."""
    if _current_user_id is None:
        raise ValueError("User context not set")
    return _current_user_id


# Function tools for OpenAI Agents SDK
# These are stateless and call MCP handlers with user context

@function_tool
async def add_task(title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new task with a title and optional description.

    Args:
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task details (id, title, description, is_completed, created_at)
    """
    user_id = get_user_context()

    params = {
        "user_id": user_id,
        "title": title,
        "description": description
    }

    return await mcp_server.invoke_tool("add_task", params)


@function_tool
async def list_tasks(is_completed: Optional[bool] = None) -> Dict[str, Any]:
    """List all tasks or filter by completion status.

    Args:
        is_completed: Optional filter - True for completed, False for incomplete, None for all

    Returns:
        Dictionary with list of tasks
    """
    user_id = get_user_context()

    params = {"user_id": user_id}
    if is_completed is not None:
        params["is_completed"] = is_completed

    return await mcp_server.invoke_tool("list_tasks", params)


@function_tool
async def complete_task(task_id: int) -> Dict[str, Any]:
    """Mark a task as complete.

    Args:
        task_id: The ID of the task to complete

    Returns:
        Dictionary with updated task details
    """
    user_id = get_user_context()

    params = {
        "user_id": user_id,
        "task_id": task_id
    }

    return await mcp_server.invoke_tool("complete_task", params)


@function_tool
async def delete_task(task_id: int) -> Dict[str, Any]:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary with deletion confirmation
    """
    user_id = get_user_context()

    params = {
        "user_id": user_id,
        "task_id": task_id
    }

    return await mcp_server.invoke_tool("delete_task", params)


@function_tool
async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    is_completed: Optional[bool] = None
) -> Dict[str, Any]:
    """Update task properties (title, description, completion status).

    Args:
        task_id: The ID of the task to update
        title: Optional new title
        description: Optional new description
        is_completed: Optional new completion status

    Returns:
        Dictionary with updated task details
    """
    user_id = get_user_context()

    params = {"user_id": user_id, "task_id": task_id}
    if title is not None:
        params["title"] = title
    if description is not None:
        params["description"] = description
    if is_completed is not None:
        params["is_completed"] = is_completed

    return await mcp_server.invoke_tool("update_task", params)


def create_task_agent() -> Agent:
    """Create an OpenAI Agents SDK Agent for task management.

    Returns:
        Agent instance configured with task management functions
    """
    return Agent(
        name="TodoChatAgent",
        instructions=SYSTEM_PROMPT,
        model=model,
        tools=[
            add_task,
            list_tasks,
            complete_task,
            delete_task,
            update_task
        ]
    )


todoChatAgent = Agent(
        name="TodoChatAgent",
        instructions=SYSTEM_PROMPT,
        model=model,
        tools=[
            add_task,
            list_tasks,
            complete_task,
            delete_task,
            update_task
        ]
    )