"""Task-related Pydantic schemas.

Schemas for task creation, updates, and responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """Task creation request schema.

    Attributes:
        title: Task title (required)
        description: Task description (optional)
        deadline: Task deadline (optional)
    """
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Task update request schema.

    All fields are optional for partial updates.

    Attributes:
        title: Updated task title
        description: Updated task description
        status: Updated task status
        priority: Updated task priority
        deadline: Updated deadline
        estimated_duration: Updated estimated hours
    """
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = Field(None, ge=1, le=999)


class TaskResponse(BaseModel):
    """Task response schema.

    Attributes:
        id: Task UUID
        title: Task title
        description: Task description
        status: Current task status
        priority: Task priority
        deadline: Task deadline
        estimated_duration: Estimated hours to complete
        completed_at: Timestamp when completed (null if not completed)
        ai_priority: AI-generated priority suggestion
        ai_estimated_duration: AI-generated duration estimate (hours)
        owner_id: UUID of task owner
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """
    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    deadline: Optional[datetime]
    estimated_duration: Optional[int]
    completed_at: Optional[datetime]
    ai_priority: Optional[TaskPriority]
    ai_estimated_duration: Optional[int]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskInDB(TaskResponse):
    """Task database schema (internal use).

    Extends TaskResponse with additional database fields if needed.
    """
    pass

    class Config:
        from_attributes = True


class TaskListParams(BaseModel):
    """Task list query parameters.

    Attributes:
        status: Filter by task status
        priority: Filter by task priority
        skip: Number of items to skip
        limit: Number of items to return
    """
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
