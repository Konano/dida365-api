"""Countdown-related models for the API client."""

from typing import List, Optional

from pydantic import Field

from .base import BaseApiModel, SortableMixin, TimestampMixin


class Countdown(BaseApiModel, SortableMixin, TimestampMixin):
    """Model for a countdown event.

    Example:
        ```python
        countdown = Countdown(
            id="countdown-1",
            type=0,
            name="Birthday",
            date=20260407,
            color="#4D8CF5",
        )
        ```
    """

    id: str = Field(..., description="Countdown identifier")
    type: int = Field(default=0, description="Countdown type")
    icon_res: Optional[str] = Field(None, description="Icon resource")
    color: Optional[str] = Field(None, description="Countdown color")
    name: str = Field(..., description="Countdown name")
    date: int = Field(default=0, description="Date in YYYYMMDD format")
    ignore_year: bool = Field(default=False, description="Whether to ignore year")
    show_calendar_type: Optional[int] = Field(None, description="Show calendar type")
    reminders: List[str] = Field(default_factory=list, description="Reminders")
    annoying_alert: Optional[int] = Field(None, description="Annoying alert")
    repeat_flag: Optional[str] = Field(None, description="Recurring rules")
    remark: Optional[str] = Field(None, description="Remark")
    status: Optional[int] = Field(None, description="Countdown status")
    style: Optional[str] = Field(None, description="Style")
    style_color: List[str] = Field(default_factory=list, description="Style colors")
    date_display_format: Optional[str] = Field(None, description="Date display format")
    timer_mode: Optional[int] = Field(None, description="Timer mode")
    show_age: bool = Field(default=False, description="Whether to show age")
    days_option: Optional[int] = Field(None, description="Days option")
    show_remark: bool = Field(default=False, description="Whether to show remark")
