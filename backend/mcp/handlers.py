"""MCP tool handlers for task management operations.

This module implements the actual logic for each MCP tool.
Handlers interact with the database to perform task operations.
"""

from typing import Dict, Any
from sqlmodel import Session, select
from app.models import Task, User
from app.database import engine
from datetime import datetime


async def handle_add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle add_task tool invocation.

    Creates a new task for the specified user.

    Args:
        params: Dictionary with user_id, title, and optional description

    Returns:
        Dictionary with task details (id, title, description, is_completed, created_at)

    Raises:
        ValueError: If user does not exist
        Exception: If database operation fails
    """
    user_id = params["user_id"]
    title = params["title"]
    description = params.get("description")

    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} does not exist")

        # Create task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            is_completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "created_at": task.created_at.isoformat()
        }


async def handle_list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle list_tasks tool invocation.

    Lists tasks for the specified user with optional filters.

    Args:
        params: Dictionary with user_id and optional is_completed filter

    Returns:
        Dictionary with tasks array and count
    """
    user_id = params["user_id"]
    is_completed = params.get("is_completed")

    with Session(engine) as session:
        # Build query
        statement = select(Task).where(Task.user_id == user_id)

        if is_completed is not None:
            statement = statement.where(Task.is_completed == is_completed)

        # Execute query
        tasks = session.exec(statement).all()

        return {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed
                }
                for task in tasks
            ],
            "count": len(tasks)
        }


async def handle_complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle complete_task tool invocation.

    Marks a task as complete.

    Args:
        params: Dictionary with user_id and task_id

    Returns:
        Dictionary with updated task details

    Raises:
        ValueError: If task does not exist or does not belong to user
    """
    user_id = params["user_id"]
    task_id = params["task_id"]

    with Session(engine) as session:
        # Get task with user isolation
        task = session.get(Task, task_id)

        if not task:
            raise ValueError(f"Task with id {task_id} does not exist")

        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Update task
        task.is_completed = True
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "is_completed": task.is_completed
        }


async def handle_delete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle delete_task tool invocation.

    Deletes a task.

    Args:
        params: Dictionary with user_id and task_id

    Returns:
        Dictionary with success status and message

    Raises:
        ValueError: If task does not exist or does not belong to user
    """
    user_id = params["user_id"]
    task_id = params["task_id"]

    with Session(engine) as session:
        # Get task with user isolation
        task = session.get(Task, task_id)

        if not task:
            raise ValueError(f"Task with id {task_id} does not exist")

        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Delete task
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task {task_id} deleted successfully"
        }


async def handle_update_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle update_task tool invocation.

    Updates task properties (title, description, completion status).

    Args:
        params: Dictionary with user_id, task_id, and optional title/description/is_completed

    Returns:
        Dictionary with updated task details

    Raises:
        ValueError: If task does not exist or does not belong to user
    """
    user_id = params["user_id"]
    task_id = params["task_id"]

    with Session(engine) as session:
        # Get task with user isolation
        task = session.get(Task, task_id)

        if not task:
            raise ValueError(f"Task with id {task_id} does not exist")

        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Update fields if provided
        if "title" in params:
            task.title = params["title"]
        if "description" in params:
            task.description = params["description"]
        if "is_completed" in params:
            task.is_completed = params["is_completed"]

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed
        }


# Tool handler registry
TOOL_HANDLERS = {
    "add_task": handle_add_task,
    "list_tasks": handle_list_tasks,
    "complete_task": handle_complete_task,
    "delete_task": handle_delete_task,
    "update_task": handle_update_task
}
