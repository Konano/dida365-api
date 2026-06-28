"""Task-related models for the API client."""

from datetime import datetime, timezone
from enum import IntEnum
from typing import List, Optional

from pydantic import Field, field_serializer

from .base import BaseApiModel, SortableMixin, TimestampMixin


class TaskPriority(IntEnum):
    """Task priority levels."""

    NONE = 0
    LOW = 1
    MEDIUM = 3
    HIGH = 5


class TaskStatus(IntEnum):
    """Task status values."""

    ABANDONED = -1  # Not mentioned in the API docs, but observed in practice
    NORMAL = 0
    COMPLETED = 2


class TaskKind(str):
    """Task kind constants."""

    TEXT = "TEXT"
    NOTE = "NOTE"
    CHECKLIST = "CHECKLIST"


class ChecklistItemStatus(IntEnum):
    """Checklist item status values."""

    NORMAL = 0
    COMPLETED = 1


class ChecklistItem(BaseApiModel, SortableMixin):
    """Model for a checklist item (subtask)."""

    id: Optional[str] = Field(default=None, description="Checklist item identifier")
    title: str = Field(..., description="Checklist item title")
    status: ChecklistItemStatus = Field(default=ChecklistItemStatus.NORMAL, description="Completion status")
    completed_time: Optional[datetime] = Field(default=None, description="Completion timestamp")
    is_all_day: bool = Field(default=True, description="Whether the item is all-day")
    start_date: Optional[datetime] = Field(default=None, description="Start date and time")
    time_zone: Optional[str] = Field(default=None, description="Time zone")


class TaskBase(BaseApiModel, SortableMixin):
    """Base model for task data."""

    title: Optional[str] = Field(default=None, description="Task title")
    content: Optional[str] = Field(default=None, description="Task content")
    desc: Optional[str] = Field(default=None, description="Task description")
    is_all_day: bool = Field(default=True, description="Whether the task is all-day")
    start_date: Optional[datetime] = Field(default=None, description="Start date and time")
    due_date: Optional[datetime] = Field(default=None, description="Due date and time")
    time_zone: Optional[str] = Field(default=None, description="Time zone")
    reminders: List[str] = Field(default_factory=list, description="List of reminder triggers")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    repeat_flag: Optional[str] = Field(default=None, description="Recurring rules")
    priority: TaskPriority = Field(default=TaskPriority.NONE, description="Task priority")
    items: List[ChecklistItem] = Field(default_factory=list, description="List of checklist items")

    @field_serializer("start_date", "due_date")
    def serialize_datetime(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")

    @field_serializer("priority")
    def serialize_priority(self, priority: TaskPriority, _info) -> int:
        return int(priority)


class TaskCreate(TaskBase):
    """Model for creating a new task.

    Example:
        ```python
        task = TaskCreate(
            title="My Task",  # Required
            project_id="project123",  # Required
            content="Task details",
            priority=TaskPriority.HIGH
        )
        ```
    """

    title: str = Field(..., description="Task title")  # Override to make required
    project_id: str = Field(..., description="Project identifier")


class TaskUpdate(TaskBase):
    """Model for updating an existing task.

    Example:
        ```python
        update = TaskUpdate(
            id="task123",
            project_id="project123",
            title="Updated Title",  # Optional
            priority=TaskPriority.LOW
        )
        ```
    """

    id: str = Field(..., description="Task identifier")
    project_id: str = Field(..., description="Project identifier")


class Task(TaskBase, TimestampMixin):
    """Model for a complete task.

    Includes all task data including system fields like ID and timestamps.
    """

    id: str = Field(..., description="Task identifier")
    project_id: str = Field(..., description="Project identifier")
    title: str = Field(..., description="Task title")  # Override to make required
    status: TaskStatus = Field(default=TaskStatus.NORMAL, description="Task status")
    completed_time: Optional[datetime] = Field(default=None, description="Completion timestamp")
    kind: Optional[str] = Field(default=None, description="Task kind: TEXT, NOTE, or CHECKLIST")
    etag: Optional[str] = Field(default=None, description="Entity tag")


# ---- Task Move ----


class TaskMoveItem(BaseApiModel):
    """Request model for moving a single task.

    Example:
        ```python
        item = TaskMoveItem(
            from_project_id="project-1",
            to_project_id="project-2",
            task_id="task-1",
        )
        ```
    """

    from_project_id: str = Field(..., description="Source project identifier")
    to_project_id: str = Field(..., description="Destination project identifier")
    task_id: str = Field(..., description="Task identifier")


class TaskMoveResult(BaseApiModel):
    """Response model for a move operation."""

    id: str = Field(..., description="Task identifier")
    etag: str = Field(..., description="New entity tag")


# ---- Task Filter / Completed ----


class TaskFilterRequest(BaseApiModel):
    """Request model for filtering tasks.

    Example:
        ```python
        filter_req = TaskFilterRequest(
            project_ids=["project-1"],
            start_date=datetime(2026, 3, 1, tzinfo=timezone.utc),
            end_date=datetime(2026, 3, 5, tzinfo=timezone.utc),
            priority=[TaskPriority.NONE],
            tag=["urgent"],
            status=[TaskStatus.NORMAL],
        )
        ```
    """

    project_ids: Optional[List[str]] = Field(default=None, description="Filter by project IDs")
    start_date: Optional[datetime] = Field(default=None, description="Start time range (inclusive)")
    end_date: Optional[datetime] = Field(default=None, description="End time range (inclusive)")
    priority: Optional[List[TaskPriority]] = Field(default=None, description="Filter by priority levels")
    tag: Optional[List[str]] = Field(default=None, description="Filter by tags (all must match)")
    status: Optional[List[TaskStatus]] = Field(default=None, description="Filter by status codes")

    @field_serializer("start_date", "end_date")
    def serialize_datetime(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    @field_serializer("priority")
    def serialize_priority(self, priorities: Optional[List[TaskPriority]], _info) -> Optional[List[int]]:
        if priorities is None:
            return None
        return [int(p) for p in priorities]

    @field_serializer("status")
    def serialize_status(self, statuses: Optional[List[TaskStatus]], _info) -> Optional[List[int]]:
        if statuses is None:
            return None
        return [int(s) for s in statuses]


class TaskCompletedRequest(BaseApiModel):
    """Request model for listing completed tasks.

    Example:
        ```python
        req = TaskCompletedRequest(
            project_ids=["project-1"],
            start_date=datetime(2026, 3, 1, tzinfo=timezone.utc),
            end_date=datetime(2026, 3, 5, tzinfo=timezone.utc),
        )
        ```
    """

    project_ids: Optional[List[str]] = Field(default=None, description="Filter by project IDs")
    start_date: Optional[datetime] = Field(default=None, description="Start time range (inclusive)")
    end_date: Optional[datetime] = Field(default=None, description="End time range (inclusive)")

    @field_serializer("start_date", "end_date")
    def serialize_datetime(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")


# ---- Task Comments ----


class CommentCreate(BaseApiModel):
    """Request model for adding a comment to a task.

    Example:
        ```python
        comment = CommentCreate(title="This is a comment")
        ```
    """

    title: str = Field(..., description="Comment text")


class Comment(BaseApiModel, TimestampMixin):
    """Response model for a task comment."""

    id: str = Field(..., description="Comment identifier")
    user_id: Optional[int] = Field(default=None, description="User id")
    title: str = Field(..., description="Comment text")
    reply_comment_id: Optional[str] = Field(default=None, description="Reply comment identifier")
    reply_user_id: Optional[int] = Field(default=None, description="Reply user id")


# ---- Tag ----


class Tag(BaseApiModel, SortableMixin):
    """Model for a tag.

    Example:
        ```python
        tag = Tag(name="work", label="work", color="#F18181", type=1)
        ```
    """

    name: str = Field(..., description="Tag name")
    label: str = Field(..., description="Tag label")
    color: Optional[str] = Field(default=None, description="Tag color")
    parent: Optional[str] = Field(default=None, description="Parent tag name")
    type: int = Field(default=1, description="Tag type: Personal=1, Team=2")


class TagCreate(BaseApiModel):
    """Model for creating a new tag.

    Example:
        ```python
        tag = TagCreate(name="urgent", label="urgent")
        ```
    """

    name: str = Field(..., description="Tag name (max 64 characters, lowercase, trimmed)")
    label: str = Field(..., description="Tag label (max 64 characters, must match name when lowercased)")
