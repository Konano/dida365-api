"""Main client module for the API."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .auth import OAuth2Manager, TokenInfo
from .config import ApiConfig, ServiceType
from .exceptions import ValidationError
from .http import HttpClient
from .logger import logger
from .models.countdown import Countdown
from .models.focus import Focus, FocusCreate, FocusType
from .models.habit import (
    Habit,
    HabitCheckin,
    HabitCheckinCreate,
    HabitCreate,
    HabitUpdate,
)
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
    ProjectUpdate,
)
from .models.task import (
    Comment,
    CommentCreate,
    Tag,
    TagCreate,
    Task,
    TaskCompletedRequest,
    TaskCreate,
    TaskFilterRequest,
    TaskMoveItem,
    TaskMoveResult,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from .settings import settings


class Dida365Client:
    """Client for interacting with the Dida365/TickTick API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        service_type: Optional[ServiceType] = None,
        access_token: Optional[str] = None,
        redirect_uri: str = "http://localhost:8080/callback",
        save_to_env: bool = True,
    ):
        """Initialize the client.

        Args:
            client_id: OAuth2 client ID (can be set via DIDA365_CLIENT_ID env var)
            client_secret: OAuth2 client secret (can be set via DIDA365_CLIENT_SECRET env var)
            service_type: Service type (dida365 or ticktick)
            access_token: OAuth2 access token (can be set via DIDA365_ACCESS_TOKEN env var).
                Constructor arg takes priority over env var.
            redirect_uri: OAuth2 redirect URI
            save_to_env: Whether to save credentials and token to .env file.
                When False, new tokens from auth are printed to stdout.
        """
        self.save_to_env = save_to_env

        # Try to get credentials from args or env
        self.client_id = client_id or settings.client_id
        self.client_secret = client_secret or settings.client_secret
        self.service_type = service_type or settings.service_type

        if not self.client_id or not self.client_secret:
            raise ValidationError(
                "Client ID and secret must be provided either through constructor "
                "or environment variables (DIDA365_CLIENT_ID, DIDA365_CLIENT_SECRET)"
            )

        self.config = ApiConfig(service_type=self.service_type)
        self.auth = OAuth2Manager(
            client_id=self.client_id, client_secret=self.client_secret, config=self.config, redirect_uri=redirect_uri
        )
        self.http = HttpClient(config=self.config)

        # Load token: constructor arg takes priority over env var
        token = access_token or settings.access_token
        if token and self._verify_token_client():
            logger.debug("Loading existing token from %s", "constructor" if access_token else "environment")
            self.auth.token = TokenInfo(
                access_token=token,
                token_type="Bearer",
                expires_in=3600,  # Default 1 hour
                scope="tasks:write tasks:read",
            )
            self.http.token = token

    def _verify_token_client(self) -> bool:
        """Verify that the token in env belongs to current client_id."""
        env_client_id = settings.client_id
        return bool(env_client_id and env_client_id == self.client_id)

    def _update_env_file(self, access_token: Optional[str] = None) -> None:
        """Update or create .env file with credentials and token.

        Args:
            access_token: Optional new access token to save
        """
        if not self.save_to_env:
            return

        env_path = Path(".env")
        existing_lines = []

        # Read existing env file if it exists
        if env_path.exists():
            with open(env_path, "r") as f:
                existing_lines = f.readlines()

        # Helper to update or add a variable
        def update_var(lines: List[str], key: str, value: str) -> List[str]:
            if not value:
                return lines
            new_line = f"{key}={value}\n"
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = new_line
                    break
            else:
                lines.append(new_line)
            return lines

        # Update credentials and token
        lines = existing_lines
        lines = update_var(lines, "DIDA365_CLIENT_ID", self.client_id)
        lines = update_var(lines, "DIDA365_CLIENT_SECRET", self.client_secret)
        lines = update_var(
            lines, "DIDA365_SERVICE_TYPE", "ticktick" if self.config.service_type == ServiceType.TICKTICK else "dida365"
        )  # Update service type
        if access_token:
            lines = update_var(lines, "DIDA365_ACCESS_TOKEN", access_token)

        # Write back to file
        with open(env_path, "w") as f:
            f.writelines(lines)

        logger.debug("Updated .env file with new credentials/token")

    async def authenticate(
        self, scope: str = "tasks:write tasks:read", state: str = "state", port: int = 8080
    ) -> TokenInfo:
        """Complete OAuth2 authentication flow."""
        token_info = await self.auth.authenticate(scope=scope, state=state, port=port)
        if token_info:
            await self.http.set_token(token_info.access_token)
            if self.save_to_env:
                self._update_env_file(access_token=token_info.access_token)
            else:
                print(f"Access token: {token_info.access_token}")
        return token_info

    async def exchange_code(self, code: str) -> TokenInfo:
        """Exchange authorization code for access token."""
        if not self.save_to_env:
            logger.warning(
                "save_to_env=False will print the token to stdout. "
                "In practice the token appears to be long-lived and exchange_code is rarely called, "
                "so this is kept as-is for now."
            )
        token_info = await self.auth.exchange_code(code)
        if token_info:
            await self.http.set_token(token_info.access_token)
            if self.save_to_env:
                self._update_env_file(access_token=token_info.access_token)
            else:
                print(f"Access token: {token_info.access_token}")
        return token_info

    # Task-related methods

    async def get_task(self, project_id: str, task_id: str) -> Task:
        """Get a task by project ID and task ID."""
        task = await self.http.get(
            f"project/{project_id}/task/{task_id}",
            model=Task,
        )
        return task

    async def create_task(self, task: TaskCreate) -> Optional[Task]:
        """Create a new task."""
        created_task = await self.http.post(
            "task",
            json_data=task.model_dump(by_alias=True, exclude_none=True),
            model=Task,
        )
        return created_task

    async def update_task(self, task: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        updated_task = await self.http.post(
            f"task/{task.id}",
            json_data=task.model_dump(by_alias=True, exclude_unset=True),
            model=Task,
        )
        return updated_task

    async def complete_task(self, project_id: str, task_id: str) -> None:
        """Mark a task as completed."""
        await self.http.post(f"project/{project_id}/task/{task_id}/complete")

    async def delete_task(self, project_id: str, task_id: str) -> None:
        """Delete a task."""
        await self.http.delete(f"project/{project_id}/task/{task_id}")

    async def move_task(self, items: List[TaskMoveItem]) -> List[TaskMoveResult]:
        """Move one or more tasks between projects.

        Args:
            items: List of TaskMoveItem specifying tasks to move.

        Returns:
            List of TaskMoveResult with task ID and new etag.
        """
        results = await self.http.post(
            "task/move",
            json_data=[item.model_dump(by_alias=True, exclude_none=True) for item in items],
            model=List[TaskMoveResult],
        )
        return results or []

    async def get_completed_tasks(
        self,
        project_ids: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Task]:
        """Get tasks marked as completed within a given time range.

        Args:
            project_ids: Optional list of project identifiers to filter by.
            start_date: Start time range (inclusive). Filters where completedTime ≥ startDate.
            end_date: End time range (inclusive). Filters where completedTime ≤ endDate.

        Returns:
            List of completed Task objects.
        """
        request = TaskCompletedRequest(
            project_ids=project_ids,
            start_date=start_date,
            end_date=end_date,
        )
        results = await self.http.post(
            "task/completed",
            json_data=request.model_dump(by_alias=True, exclude_none=True),
            model=List[Task],
        )
        return results or []

    async def filter_tasks(
        self,
        project_ids: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[List[TaskPriority]] = None,
        tag: Optional[List[str]] = None,
        status: Optional[List[TaskStatus]] = None,
    ) -> List[Task]:
        """Filter tasks with advanced criteria.

        Args:
            project_ids: Filter by project IDs.
            start_date: Filters tasks where startDate ≥ value.
            end_date: Filters tasks where startDate ≤ value.
            priority: Filter by priority levels (None=0, Low=1, Medium=3, High=5).
            tag: Filter by tags (all specified tags must match).
            status: Filter by status codes (Normal=0, Completed=2).

        Returns:
            List of matching Task objects.
        """
        request = TaskFilterRequest(
            project_ids=project_ids,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            tag=tag,
            status=status,
        )
        results = await self.http.post(
            "task/filter",
            json_data=request.model_dump(by_alias=True, exclude_none=True),
            model=List[Task],
        )
        return results or []

    async def get_task_comments(self, project_id: str, task_id: str) -> List[Comment]:
        """Get comments for a task.

        Args:
            project_id: Project identifier.
            task_id: Task identifier.

        Returns:
            List of Comment objects.
        """
        results = await self.http.get(
            f"project/{project_id}/task/{task_id}/comments",
            model=List[Comment],
        )
        return results

    async def add_task_comment(self, project_id: str, task_id: str, title: str) -> Optional[Comment]:
        """Add a comment to a task.

        Args:
            project_id: Project identifier.
            task_id: Task identifier.
            title: Comment text.

        Returns:
            The created Comment.
        """
        comment = CommentCreate(title=title)
        return await self.http.post(
            f"project/{project_id}/task/{task_id}/comment",
            json_data=comment.model_dump(by_alias=True, exclude_none=True),
            model=Comment,
        )

    async def delete_task_comment(self, project_id: str, task_id: str, comment_id: str) -> None:
        """Delete a comment from a task.

        Args:
            project_id: Project identifier.
            task_id: Task identifier.
            comment_id: Comment identifier.
        """
        await self.http.delete(f"project/{project_id}/task/{task_id}/comment/{comment_id}")

    # Tag methods

    async def get_tags(self) -> List[Tag]:
        """Get all tags.

        Returns:
            List of Tag objects.
        """
        tags = await self.http.get("tag", model=List[Tag])
        return tags

    async def create_tag(self, tag: TagCreate) -> Optional[Tag]:
        """Create a new tag.

        Args:
            tag: TagCreate with name and label.

        Returns:
            The created Tag.
        """
        return await self.http.post(
            "tag",
            json_data=tag.model_dump(by_alias=True, exclude_none=True),
            model=Tag,
        )

    # Focus methods

    async def get_focus(self, focus_id: str, focus_type: FocusType) -> Focus:
        """Get a focus record by ID.

        Args:
            focus_id: Focus identifier.
            focus_type: Focus type (Pomodoro=0 or Timing=1).

        Returns:
            The Focus record.
        """
        focus = await self.http.get(f"focus/{focus_id}", params={"type": str(focus_type.value)}, model=Focus)
        return focus

    async def get_focuses(self, from_date: str, to_date: str, focus_type: FocusType) -> List[Focus]:
        """Get focus records within a time range.

        Args:
            from_date: Range start time, e.g. "2026-04-01T00:00:00+0800".
            to_date: Range end time, e.g. "2026-04-02T00:00:00+0800".
            focus_type: Focus type (Pomodoro=0 or Timing=1).

        Returns:
            List of Focus records.
        """
        results = await self.http.get(
            "focus",
            params={"from": from_date, "to": to_date, "type": str(focus_type.value)},
            model=List[Focus],
        )
        return results

    async def create_focus(self, focus: FocusCreate) -> Optional[Focus]:
        """Create a new focus record.

        Args:
            focus: FocusCreate with type, times, and optional task/note.

        Returns:
            The created Focus.
        """
        return await self.http.post(
            "focus",
            json_data=focus.model_dump(by_alias=True, exclude_none=True),
            model=Focus,
        )

    async def delete_focus(self, focus_id: str, focus_type: FocusType) -> None:
        """Delete a focus record.

        Args:
            focus_id: Focus identifier.
            focus_type: Focus type (Pomodoro=0 or Timing=1).
        """
        await self.http.delete(f"focus/{focus_id}", params={"type": str(focus_type.value)})

    # Countdown methods

    async def get_countdowns(self) -> List[Countdown]:
        """Get all countdown events.

        Returns:
            List of Countdown objects.
        """
        items = await self.http.get("countdown", model=List[Countdown])
        return items

    # Habit methods

    async def get_habit(self, habit_id: str) -> Habit:
        """Get a habit by ID.

        Args:
            habit_id: Habit identifier.

        Returns:
            The Habit record.
        """
        habit = await self.http.get(f"habit/{habit_id}", model=Habit)
        return habit

    async def get_all_habits(self) -> List[Habit]:
        """Get all habits.

        Returns:
            List of Habit objects.
        """
        habits = await self.http.get("habit", model=List[Habit])
        return habits

    async def create_habit(self, habit: HabitCreate) -> Optional[Habit]:
        """Create a new habit.

        Args:
            habit: HabitCreate with name and optional settings.

        Returns:
            The created Habit.
        """
        return await self.http.post(
            "habit",
            json_data=habit.model_dump(by_alias=True, exclude_none=True),
            model=Habit,
        )

    async def update_habit(self, habit_id: str, habit: HabitUpdate) -> Optional[Habit]:
        """Update an existing habit.

        Args:
            habit_id: Habit identifier.
            habit: HabitUpdate with fields to update.

        Returns:
            The updated Habit.
        """
        return await self.http.post(
            f"habit/{habit_id}",
            json_data=habit.model_dump(by_alias=True, exclude_none=True),
            model=Habit,
        )

    async def create_or_update_habit_checkin(
        self, habit_id: str, checkin: HabitCheckinCreate
    ) -> Optional[HabitCheckin]:
        """Create or update a habit check-in.

        Args:
            habit_id: Habit identifier.
            checkin: HabitCheckinCreate with stamp and value.

        Returns:
            The HabitCheckin result.
        """
        return await self.http.post(
            f"habit/{habit_id}/checkin",
            json_data=checkin.model_dump(by_alias=True, exclude_none=True),
            model=HabitCheckin,
        )

    async def get_habit_checkins(self, habit_ids: str, from_stamp: int, to_stamp: int) -> List[HabitCheckin]:
        """Get habit check-ins for a date range.

        Args:
            habit_ids: Comma-separated habit identifiers, e.g. "habit-1,habit-2".
            from_stamp: Start date stamp in YYYYMMDD format.
            to_stamp: End date stamp in YYYYMMDD format.

        Returns:
            List of HabitCheckin objects.
        """
        results = await self.http.get(
            "habit/checkins",
            params={"habitIds": habit_ids, "from": str(from_stamp), "to": str(to_stamp)},
            model=List[HabitCheckin],
        )
        return results

    # Project-related methods

    async def get_projects(self) -> List[Project]:
        """Get all projects."""
        projects = await self.http.get("project", model=List[Project])
        return projects

    async def get_project(self, project_id: str) -> Project:
        """Get a project by ID."""
        return await self.http.get(f"project/{project_id}", model=Project)

    async def get_project_with_data(self, project_id: str) -> ProjectData:
        """Get a project with its tasks and columns."""
        data = await self.http.get(f"project/{project_id}/data", model=ProjectData)
        return data

    async def create_project(self, project: ProjectCreate) -> Optional[Project]:
        """Create a new project."""
        created_project = await self.http.post(
            "project",
            json_data=project.model_dump(by_alias=True, exclude_none=True),
            model=Project,
        )
        return created_project

    async def update_project(self, project: ProjectUpdate) -> Optional[Project]:
        """Update an existing project."""
        updated_project = await self.http.post(
            f"project/{project.id}",
            json_data=project.model_dump(by_alias=True, exclude_none=True),
            model=Project,
        )
        return updated_project

    async def delete_project(self, project_id: str) -> None:
        """Delete a project."""
        await self.http.delete(f"project/{project_id}")

    # Project Group methods

    async def get_project_groups(self) -> List[ProjectGroup]:
        """Get all project groups.

        Returns:
            List of ProjectGroup objects.
        """
        groups = await self.http.get("project/group", model=List[ProjectGroup])
        return groups

    async def create_project_group(self, group: ProjectGroupCreate) -> Optional[ProjectGroup]:
        """Create a new project group.

        Args:
            group: ProjectGroupCreate with the group name.

        Returns:
            The created ProjectGroup.
        """
        return await self.http.post(
            "project/group",
            json_data=group.model_dump(by_alias=True, exclude_none=True),
            model=ProjectGroup,
        )

    async def update_project_group(self, group_id: str, group: ProjectGroupUpdate) -> Optional[ProjectGroup]:
        """Update an existing project group.

        Args:
            group_id: Project group identifier.
            group: ProjectGroupUpdate with fields to update.

        Returns:
            The updated ProjectGroup.
        """
        return await self.http.post(
            f"project/group/{group_id}",
            json_data=group.model_dump(by_alias=True, exclude_none=True),
            model=ProjectGroup,
        )

    async def delete_project_group(self, group_id: str) -> None:
        """Delete a project group.

        Args:
            group_id: Project group identifier.
        """
        await self.http.delete(f"project/group/{group_id}")

    # Column methods

    async def get_columns(self, project_id: str) -> List[Column]:
        """Get columns for a project.

        Args:
            project_id: Project identifier.

        Returns:
            List of Column objects.
        """
        cols = await self.http.get(f"project/{project_id}/column", model=List[Column])
        return cols

    async def create_column(self, project_id: str, column: ColumnCreate) -> Optional[Column]:
        """Create a new column in a project.

        Args:
            project_id: Project identifier.
            column: ColumnCreate with the column name.

        Returns:
            The created Column.
        """
        return await self.http.post(
            f"project/{project_id}/column",
            json_data=column.model_dump(by_alias=True, exclude_none=True),
            model=Column,
        )

    async def update_column(self, project_id: str, column_id: str, column: ColumnUpdate) -> Optional[Column]:
        """Update an existing column.

        Args:
            project_id: Project identifier.
            column_id: Column identifier.
            column: ColumnUpdate with fields to update.

        Returns:
            The updated Column.
        """
        return await self.http.post(
            f"project/{project_id}/column/{column_id}",
            json_data=column.model_dump(by_alias=True, exclude_none=True),
            model=Column,
        )

    # Authentication methods

    def get_authorization_url(
        self,
        scope: str = "tasks:write tasks:read",
        state: str = "state",
    ) -> str:
        """Get the authorization URL for OAuth2 flow."""
        return self.auth.get_authorization_url(scope=scope, state=state)
