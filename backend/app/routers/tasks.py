"""Task CRUD endpoints for FastAPI Todo API.

This module implements all task-related endpoints:
- GET /api/{user_id}/tasks - List all tasks for a user
- POST /api/{user_id}/tasks - Create a new task
- GET /api/{user_id}/tasks/{task_id} - Get task details
- PUT /api/{user_id}/tasks/{task_id} - Update task
- PATCH /api/{user_id}/tasks/{task_id}/toggle - Toggle completion
- DELETE /api/{user_id}/tasks/{task_id} - Delete task
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.dependencies.auth import get_current_user, validate_user_access

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(
    user_id: int,
    request: Request,
    session: Session = Depends(get_session)
) -> List[Task]:
    """List all tasks for a specific user.

    Args:
        user_id: ID of the user whose tasks to retrieve
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        List of tasks belonging to the user (empty list if no tasks)

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)

    Example:
        GET /api/1/tasks
        Response: [{"id": 1, "user_id": 1, "title": "Buy groceries", ...}]
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Query tasks filtered by user_id from JWT token (not URL)
    token_user_id = current_user["user_id"]
    statement = select(Task).where(Task.user_id == token_user_id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_data: TaskCreate,
    request: Request,
    session: Session = Depends(get_session)
) -> Task:
    """Create a new task for a specific user.

    Args:
        user_id: ID of the user who owns the task
        task_data: Task creation data (title, description)
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        Created task with all fields including ID and timestamps

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)

    Example:
        POST /api/1/tasks
        Body: {"title": "Buy groceries", "description": "Milk and eggs"}
        Response: {"id": 1, "user_id": 1, "title": "Buy groceries", ...}
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Create new task with user_id from JWT token (not URL)
    token_user_id = current_user["user_id"]
    task = Task(
        user_id=token_user_id,
        title=task_data.title,
        description=task_data.description,
        is_completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(
    user_id: int,
    task_id: int,
    request: Request,
    session: Session = Depends(get_session)
) -> Task:
    """Get details of a specific task.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to retrieve
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        Task details

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)
        HTTPException 404: Task not found

    Example:
        GET /api/1/tasks/1
        Response: {"id": 1, "user_id": 1, "title": "Buy groceries", ...}
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Fetch task by id
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user (double-check with JWT user_id)
    token_user_id = current_user["user_id"]
    if not task or task.user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session)
) -> Task:
    """Update an existing task.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to update
        task_data: Task update data (title, description, is_completed)
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        Updated task

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)
        HTTPException 404: Task not found

    Example:
        PUT /api/1/tasks/1
        Body: {"title": "Buy groceries and cook", "is_completed": true}
        Response: {"id": 1, "user_id": 1, "title": "Buy groceries and cook", ...}
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Fetch task by id
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user (double-check with JWT user_id)
    token_user_id = current_user["user_id"]
    if not task or task.user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{user_id}/tasks/{task_id}/toggle", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def toggle_task(
    user_id: int,
    task_id: int,
    request: Request,
    session: Session = Depends(get_session)
) -> Task:
    """Toggle task completion status.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to toggle
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        Updated task with toggled completion status

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)
        HTTPException 404: Task not found

    Example:
        PATCH /api/1/tasks/1/toggle
        Response: {"id": 1, "user_id": 1, "is_completed": true, ...}
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Fetch task by id
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user (double-check with JWT user_id)
    token_user_id = current_user["user_id"]
    if not task or task.user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    # Toggle completion status
    task.is_completed = not task.is_completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    task_id: int,
    request: Request,
    session: Session = Depends(get_session)
) -> None:
    """Delete a task permanently.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete
        request: FastAPI request (for JWT authentication)
        session: Database session (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 401: Authentication required
        HTTPException 403: Access denied (user isolation)
        HTTPException 404: Task not found

    Example:
        DELETE /api/1/tasks/1
        Response: 204 No Content
    """
    # Get authenticated user from JWT token
    current_user = get_current_user(request)

    # Validate user can access this resource (user isolation)
    validate_user_access(current_user, user_id)

    # Fetch task by id
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user (double-check with JWT user_id)
    token_user_id = current_user["user_id"]
    if not task or task.user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )

    # Delete task from database
    session.delete(task)
    session.commit()
