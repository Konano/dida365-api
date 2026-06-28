"""Project group-related models for the API client."""

from typing import Optional

from pydantic import Field

from .base import BaseApiModel, SortableMixin


class ProjectGroup(BaseApiModel, SortableMixin):
    """Model for a project group.

    Example:
        ```python
        group = ProjectGroup(
            id="group-1",
            name="Work",
            show_all=True,
            view_mode="list",
        )
        ```
    """

    id: str = Field(..., description="Project group identifier")
    name: str = Field(..., description="Project group name")
    show_all: bool = Field(default=True, description="Whether to show all projects in the group")
    view_mode: Optional[str] = Field(default="list", description="View mode: list, kanban, or timeline")


class ProjectGroupCreate(BaseApiModel):
    """Model for creating a new project group.

    Example:
        ```python
        group = ProjectGroupCreate(name="Work")
        ```
    """

    name: str = Field(..., description="Project group name (max 64 characters)")


class ProjectGroupUpdate(BaseApiModel):
    """Model for updating an existing project group.

    Example:
        ```python
        update = ProjectGroupUpdate(name="New Name")
        ```
    """

    name: Optional[str] = Field(None, description="Project group name (max 64 characters)")
