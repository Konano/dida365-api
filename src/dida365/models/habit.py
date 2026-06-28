"""Habit-related models for the API client."""

from datetime import datetime, timezone
from typing import List, Optional

from pydantic import Field, field_serializer

from .base import BaseApiModel, SortableMixin, TimestampMixin


class Habit(BaseApiModel, SortableMixin, TimestampMixin):
    """Model for a habit."""

    id: str = Field(..., description="Habit unique id")
    name: str = Field(..., description="Habit name")
    icon_res: Optional[str] = Field(None, description="Habit icon resource")
    color: Optional[str] = Field(None, description="Habit color")
    status: int = Field(default=0, description="Habit status")
    encouragement: Optional[str] = Field(None, description="Habit encouragement message")
    total_check_ins: int = Field(default=0, description="Total check-ins")
    archived_time: Optional[datetime] = Field(None, description="Archived time")
    type: Optional[str] = Field(None, description="Habit type")
    goal: float = Field(default=1.0, description="Habit goal")
    step: float = Field(default=1.0, description="Habit step")
    unit: Optional[str] = Field(None, description="Habit unit")
    etag: Optional[str] = Field(None, description="Habit etag")
    repeat_rule: Optional[str] = Field(None, description="Habit repeat rule")
    reminders: List[str] = Field(default_factory=list, description="Habit reminders")
    record_enable: bool = Field(default=False, description="Whether record is enabled")
    section_id: Optional[str] = Field(None, description="Habit section identifier")
    target_days: int = Field(default=0, description="Target days")
    target_start_date: Optional[int] = Field(None, description="Target start date in YYYYMMDD format")
    completed_cycles: int = Field(default=0, description="Completed cycles")
    ex_dates: List[str] = Field(default_factory=list, description="Excluded dates")
    style: int = Field(default=0, description="Habit style")


class HabitCreate(BaseApiModel):
    """Model for creating a new habit.

    Example:
        ```python
        habit = HabitCreate(
            name="Read",
            type="Boolean",
            goal=1.0,
            step=1.0,
            unit="Count",
            repeat_rule="RRULE:FREQ=DAILY;INTERVAL=1",
        )
        ```
    """

    name: str = Field(..., description="Habit name (max 1000 characters)")
    icon_res: Optional[str] = Field(None, description="Habit icon resource")
    color: Optional[str] = Field(None, description="Habit color")
    sort_order: Optional[int] = Field(None, description="Habit sort order")
    status: Optional[int] = Field(None, description="Habit status")
    encouragement: Optional[str] = Field(None, description="Habit encouragement message")
    type: Optional[str] = Field(None, description="Habit type")
    goal: Optional[float] = Field(None, description="Habit goal")
    step: Optional[float] = Field(None, description="Habit step")
    unit: Optional[str] = Field(None, description="Habit unit")
    repeat_rule: Optional[str] = Field(None, description="Habit repeat rule")
    reminders: Optional[List[str]] = Field(None, description="Habit reminders")
    record_enable: Optional[bool] = Field(None, description="Whether record is enabled")
    section_id: Optional[str] = Field(None, description="Habit section identifier")
    target_days: Optional[int] = Field(None, description="Target days")
    target_start_date: Optional[int] = Field(None, description="Target start date in YYYYMMDD format")
    completed_cycles: Optional[int] = Field(None, description="Completed cycles")
    ex_dates: Optional[List[str]] = Field(None, description="Excluded dates")
    style: Optional[int] = Field(None, description="Habit style")


class HabitUpdate(BaseApiModel):
    """Model for updating an existing habit.

    Example:
        ```python
        update = HabitUpdate(name="Read more", goal=2.0)
        ```
    """

    name: Optional[str] = Field(None, description="Habit name (max 1000 characters)")
    icon_res: Optional[str] = Field(None, description="Habit icon resource")
    color: Optional[str] = Field(None, description="Habit color")
    sort_order: Optional[int] = Field(None, description="Habit sort order")
    status: Optional[int] = Field(None, description="Habit status")
    encouragement: Optional[str] = Field(None, description="Habit encouragement message")
    type: Optional[str] = Field(None, description="Habit type")
    goal: Optional[float] = Field(None, description="Habit goal")
    step: Optional[float] = Field(None, description="Habit step")
    unit: Optional[str] = Field(None, description="Habit unit")
    repeat_rule: Optional[str] = Field(None, description="Habit repeat rule")
    reminders: Optional[List[str]] = Field(None, description="Habit reminders")
    record_enable: Optional[bool] = Field(None, description="Whether record is enabled")
    section_id: Optional[str] = Field(None, description="Habit section identifier")
    target_days: Optional[int] = Field(None, description="Target days")
    target_start_date: Optional[int] = Field(None, description="Target start date in YYYYMMDD format")
    completed_cycles: Optional[int] = Field(None, description="Completed cycles")
    ex_dates: Optional[List[str]] = Field(None, description="Excluded dates")
    style: Optional[int] = Field(None, description="Habit style")


class HabitCheckinData(BaseApiModel):
    """Model for a single check-in entry."""

    id: Optional[str] = Field(None, description="Check-in id")
    stamp: int = Field(..., description="Date stamp in YYYYMMDD format")
    time: Optional[datetime] = Field(None, description="Check-in time")
    op_time: Optional[datetime] = Field(None, description="Operation time")
    value: float = Field(default=1.0, description="Check-in value")
    goal: float = Field(default=1.0, description="Check-in goal")
    status: Optional[int] = Field(None, description="Check-in status")


class HabitCheckin(BaseApiModel, TimestampMixin):
    """Model for a habit check-in document."""

    id: Optional[str] = Field(None, description="Check-in document id")
    habit_id: str = Field(..., description="Habit id")
    etag: Optional[str] = Field(None, description="Check-in etag")
    year: int = Field(default=0, description="Year")
    checkins: List[HabitCheckinData] = Field(default_factory=list, description="Check-in entries")


class HabitCheckinCreate(BaseApiModel):
    """Model for creating or updating a habit check-in.

    Example:
        ```python
        checkin = HabitCheckinCreate(stamp=20260407, value=1.0, goal=1.0)
        ```
    """

    stamp: int = Field(..., description="Date stamp in YYYYMMDD format")
    time: Optional[datetime] = Field(None, description="Check-in time")
    op_time: Optional[datetime] = Field(None, description="Operation time")
    value: Optional[float] = Field(default=1.0, description="Check-in value")
    goal: Optional[float] = Field(default=1.0, description="Check-in goal")
    status: Optional[int] = Field(None, description="Check-in status")

    @field_serializer("time", "op_time")
    def serialize_datetime(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")
