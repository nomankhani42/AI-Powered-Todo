"""Task management API endpoints.

Handles task CRUD operations: create, read, update, delete.
"""

import asyncio
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.session import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListParams
from app.schemas.shared import PaginatedResponse
from app.dependencies import get_current_user
from app.services.task_service import (
    create_task as create_task_service,
    get_task as get_task_service,
    get_user_tasks as get_user_tasks_service,
    update_task as update_task_service,
    delete_task as delete_task_service,
)
from app.services.ai_service import generate_priority_and_duration
from app.utils.logger import logger

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    tags=["Tasks"],
)
async def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task for the authenticated user.

    Automatically generates AI-powered suggestions for priority and duration
    estimation based on the task description.

    **Request Body**:
    - `title`: Task title (required)
    - `description`: Task description (optional)
    - `deadline`: Task deadline (optional, ISO 8601 format)

    **Response**: Created task with AI suggestions (201 Created)

    **Errors**:
    - 401: Unauthorized
    - 400: Invalid request data
    """
    logger.info(f"Creating task for user {user.email}: {task_data.title}")

    # Create task in database
    task = create_task_service(
        db=db,
        user_id=user.id,
        title=task_data.title,
        description=task_data.description,
        deadline=task_data.deadline,
    )

    # Generate AI suggestions asynchronously (non-blocking)
    # Fire and forget to avoid blocking the response
    asyncio.create_task(
        _generate_and_update_ai_suggestions(db, task.id, user.id, task_data)
    )

    logger.info(f"Task created: {task.id}")
    return TaskResponse.model_validate(task)


async def _generate_and_update_ai_suggestions(
    db: Session,
    task_id: UUID,
    user_id: UUID,
    task_data: TaskCreate,
):
    """Background task to generate and update AI suggestions."""
    try:
        # Generate AI suggestions
        description_for_ai = f"{task_data.title}. {task_data.description or ''}"
        priority, duration = await generate_priority_and_duration(description_for_ai)

        if priority and duration:
            # Update task with AI suggestions
            from app.services.task_service import update_ai_suggestions
            from app.models.task import TaskPriority as TaskPriorityEnum

            update_ai_suggestions(
                db,
                task_id,
                user_id,
                priority=TaskPriorityEnum(priority),
                estimated_duration=duration,
            )
            logger.info(f"AI suggestions updated for task {task_id}")
    except Exception as e:
        logger.error(f"Error generating AI suggestions for task {task_id}: {e}")
        # Don't raise - graceful degradation


@router.get(
    "/",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List user's tasks",
    tags=["Tasks"],
)
async def list_tasks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: TaskStatus | None = Query(None, alias="status"),
    priority_filter: TaskPriority | None = Query(None, alias="priority"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """List all tasks for the authenticated user with optional filtering.

    **Query Parameters**:
    - `status`: Filter by status (pending, in_progress, completed)
    - `priority`: Filter by priority (low, medium, high, urgent)
    - `skip`: Number of items to skip (default: 0)
    - `limit`: Number of items to return (default: 20, max: 100)

    **Response**: Paginated list of tasks (200 OK)

    **Errors**:
    - 401: Unauthorized
    """
    logger.info(
        f"Listing tasks for user {user.email}: status={status_filter}, priority={priority_filter}"
    )

    tasks, total = get_user_tasks_service(
        db=db,
        user_id=user.id,
        status=status_filter,
        priority=priority_filter,
        skip=skip,
        limit=limit,
    )

    return PaginatedResponse[TaskResponse](
        items=[TaskResponse.model_validate(task) for task in tasks],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task details",
    tags=["Tasks"],
)
async def get_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get details of a specific task.

    **Path Parameters**:
    - `task_id`: UUID of the task

    **Response**: Task details (200 OK)

    **Errors**:
    - 401: Unauthorized
    - 404: Task not found
    - 403: User doesn't have access to this task
    """
    logger.info(f"Getting task {task_id} for user {user.email}")

    task = get_task_service(db=db, task_id=task_id, user_id=user.id)

    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    tags=["Tasks"],
)
async def update_task(
    task_id: UUID,
    task_updates: TaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a specific task.

    Only the task owner can update tasks.

    **Path Parameters**:
    - `task_id`: UUID of the task

    **Request Body**: Task fields to update (all optional)
    - `title`, `description`, `status`, `priority`, `deadline`, `estimated_duration`

    **Response**: Updated task (200 OK)

    **Errors**:
    - 401: Unauthorized
    - 404: Task not found
    - 403: User is not the task owner
    """
    logger.info(f"Updating task {task_id} for user {user.email}")

    # Prepare update dict (exclude None values)
    updates = {k: v for k, v in task_updates.model_dump().items() if v is not None}

    task = update_task_service(db=db, task_id=task_id, user_id=user.id, **updates)

    logger.info(f"Task updated: {task_id}")
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    tags=["Tasks"],
)
async def delete_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific task.

    Only the task owner can delete tasks.

    **Path Parameters**:
    - `task_id`: UUID of the task

    **Response**: No content (204 No Content)

    **Errors**:
    - 401: Unauthorized
    - 404: Task not found
    - 403: User is not the task owner
    """
    logger.info(f"Deleting task {task_id} for user {user.email}")

    delete_task_service(db=db, task_id=task_id, user_id=user.id)

    logger.info(f"Task deleted: {task_id}")
