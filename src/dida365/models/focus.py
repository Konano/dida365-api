"""Focus-related models for the API client."""

from datetime import datetime, timezone
from enum import IntEnum
from typing import List, Optional

from pydantic import Field, field_serializer

from .base import BaseApiModel, TimestampMixin


class FocusType(IntEnum):
    """Focus type."""

    POMODORO = 0
    TIMING = 1


class PomodoroTaskBrief(BaseApiModel):
    """Brief task info for a focus record."""

    task_id: str = Field(..., description="Task id")
    title: str = Field(..., description="Task title")
    habit_id: Optional[str] = Field(None, description="Habit id")
    timer_id: Optional[str] = Field(None, description="Timer id")
    timer_name: Optional[str] = Field(None, description="Timer name")
    start_time: Optional[datetime] = Field(None, description="Task focus start time")
    end_time: Optional[datetime] = Field(None, description="Task focus end time")


class Focus(BaseApiModel, TimestampMixin):
    """Model for a focus (Pomodoro/Timing) record."""

    id: str = Field(..., description="Focus unique id")
    user_id: Optional[int] = Field(None, description="User id")
    type: FocusType = Field(..., description="Focus type: Pomodoro=0, Timing=1")
    task_id: Optional[str] = Field(None, description="Task id")
    note: Optional[str] = Field(None, description="Focus note")
    tasks: List[PomodoroTaskBrief] = Field(default_factory=list, description="Related task briefs")
    status: Optional[int] = Field(None, description="Pomodoro status")
    start_time: Optional[datetime] = Field(None, description="Focus start time")
    end_time: Optional[datetime] = Field(None, description="Focus end time")
    pause_duration: int = Field(default=0, description="Pause duration in seconds")
    adjust_time: int = Field(default=0, description="Adjusted time in seconds")
    added: bool = Field(default=False, description="Whether record was added")
    etimestamp: Optional[int] = Field(None, description="Entity timestamp")
    etag: Optional[str] = Field(None, description="Entity tag")
    duration: Optional[int] = Field(None, description="Focus duration")
    relation_type: List[int] = Field(default_factory=list, description="Relation types")


class FocusCreate(BaseApiModel):
    """Model for creating a new focus record.

    Example:
        ```python
        focus = FocusCreate(
            type=FocusType.POMODORO,
            task_id="task-1",
            start_time=datetime(2026, 4, 7, 9, 0, 0, tzinfo=timezone(timedelta(hours=8))),
            end_time=datetime(2026, 4, 7, 9, 25, 0, tzinfo=timezone(timedelta(hours=8))),
            duration=1500,
        )
        ```
    """

    type: FocusType = Field(..., description="Focus type: Pomodoro=0, Timing=1")
    task_id: Optional[str] = Field(None, description="Task id")
    note: Optional[str] = Field(None, description="Focus note (max 5000 characters)")
    start_time: Optional[datetime] = Field(None, description="Focus start time")
    end_time: Optional[datetime] = Field(None, description="Focus end time")
    pause_duration: Optional[int] = Field(None, description="Pause duration in seconds")
    duration: Optional[int] = Field(None, description="Focus duration")
    relation_type: Optional[List[int]] = Field(None, description="Relation types")

    @field_serializer("type")
    def serialize_type(self, t: FocusType, _info) -> int:
        return int(t)

    @field_serializer("start_time", "end_time")
    def serialize_datetime(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0800")
