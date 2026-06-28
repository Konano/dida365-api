"""Dida365/TickTick API client package."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from .client import Dida365Client
from .config import ApiConfig, ServiceType
from .exceptions import ApiError, AuthenticationError, NotFoundError, RateLimitError, ValidationError
from .models.countdown import Countdown
from .models.focus import Focus, FocusCreate, FocusType, PomodoroTaskBrief
from .models.project import (
    Column,
    ColumnCreate,
    ColumnUpdate,
    Project,
    ProjectCreate,
    ProjectData,
    ProjectGroup,
    ProjectGroupCreate,
    ProjectGroupUpdate,
    ProjectKind,
    ProjectPermission,
    ProjectUpdate,
    ViewMode,
)
from .models.task import (
    ChecklistItem,
    Comment,
    CommentCreate,
    Tag,
    TagCreate,
    Task,
    TaskCompletedRequest,
    TaskCreate,
    TaskFilterRequest,
    TaskKind,
    TaskMoveItem,
    TaskMoveResult,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)

try:
    __version__ = _metadata_version("dida365")
except PackageNotFoundError:
    __version__ = "0.0.0"
__all__ = [
    # Main client
    "Dida365Client",
    # Configuration
    "ApiConfig",
    "ServiceType",
    # Countdown models
    "Countdown",
    # Exceptions
    "ApiError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    # Focus models
    "Focus",
    "FocusCreate",
    "FocusType",
    "PomodoroTaskBrief",
    # Project models
    "Column",
    "ColumnCreate",
    "ColumnUpdate",
    "Project",
    "ProjectCreate",
    "ProjectData",
    "ProjectGroup",
    "ProjectGroupCreate",
    "ProjectGroupUpdate",
    "ProjectKind",
    "ProjectPermission",
    "ProjectUpdate",
    "ViewMode",
    # Task models
    "ChecklistItem",
    "Comment",
    "CommentCreate",
    "Tag",
    "TagCreate",
    "Task",
    "TaskCompletedRequest",
    "TaskCreate",
    "TaskFilterRequest",
    "TaskKind",
    "TaskMoveItem",
    "TaskMoveResult",
    "TaskPriority",
    "TaskStatus",
    "TaskUpdate",
]
