# Models API Reference

## Project Models

### Project

Base project model representing a project in TickTick/Dida365.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes | Project identifier |
| `name` | str | Yes | Project name |
| `color` | str | No | Hex color code (e.g., "#FF0000") |
| `view_mode` | ViewMode | No | View mode (LIST, KANBAN, TIMELINE) |
| `kind` | ProjectKind | No | Project kind (TASK, NOTE) |
| `closed` | bool | No | Whether project is closed |
| `group_id` | str | No | Project group identifier |
| `permission` | ProjectPermission | No | Access level |

### ProjectCreate

Model for creating a new project.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | str | Yes | Project name |
| `color` | str | No | Hex color code |
| `view_mode` | ViewMode | No | View mode |
| `kind` | ProjectKind | No | Project kind |

### ProjectUpdate

Model for updating an existing project.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes | Project identifier |
| `name` | str | No | New project name |
| `color` | str | No | New hex color code |
| `view_mode` | ViewMode | No | New view mode |
| `kind` | ProjectKind | No | New project kind |

### ProjectData

Model containing project details with tasks and columns.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `project` | Project | Yes | Project details |
| `tasks` | List[Task] | Yes | List of tasks in project |
| `columns` | List[Column] | No | List of columns (for Kanban view) |

### Column

Model representing a column in Kanban view.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes | Column identifier |
| `name` | str | Yes | Column name |
| `order` | int | No | Column order |

### Enums

#### ViewMode

```python
class ViewMode(str, Enum):
    LIST = "LIST"        # Default list view
    KANBAN = "KANBAN"    # Kanban board view
    TIMELINE = "TIMELINE" # Timeline/calendar view
```

#### ProjectKind

```python
class ProjectKind(str, Enum):
    TASK = "TASK"  # Regular task project
    NOTE = "NOTE"  # Note-taking project
```

#### ProjectPermission

```python
class ProjectPermission(str, Enum):
    READ = "READ"      # Read-only access
    WRITE = "WRITE"    # Read/write access
    COMMENT = "COMMENT" # Can comment only
```

## Task Models

### Task

Base task model representing a task in TickTick/Dida365.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes | Task identifier |
| `project_id` | str | Yes | Project identifier |
| `title` | str | Yes | Task title |
| `content` | str | No | Task content/notes |
| `desc` | str | No | Task description |
| `priority` | TaskPriority | No | Task priority level |
| `is_all_day` | bool | No | Whether task is all-day |
| `start_date` | datetime | No | Start date and time |
| `due_date` | datetime | No | Due date and time |
| `time_zone` | str | No | Time zone for dates |
| `reminders` | List[str] | No | Reminder triggers |
| `repeat_flag` | str | No | Recurring rules |
| `items` | List[ChecklistItem] | No | Checklist items |
| `status` | TaskStatus | No | Task status |

### TaskCreate

Model for creating a new task.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `project_id` | str | Yes | Project identifier |
| `title` | str | Yes | Task title |
| `content` | str | No | Task content |
| `desc` | str | No | Task description |
| `priority` | TaskPriority | No | Task priority |
| `is_all_day` | bool | No | All-day flag |
| `start_date` | datetime | No | Start time |
| `due_date` | datetime | No | Due time |
| `time_zone` | str | No | Time zone |
| `reminders` | List[str] | No | Reminders |
| `repeat_flag` | str | No | Recurring rules |
| `items` | List[ChecklistItem] | No | Checklist items |

### TaskUpdate

Model for updating an existing task.

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes | Task identifier |
| `project_id` | str | Yes | Project identifier |
| `title` | str | No | New task title |
| `content` | str | No | New content |
| `desc` | str | No | New description |
| `priority` | TaskPriority | No | New priority |
| `is_all_day` | bool | No | New all-day flag |
| `start_date` | datetime | No | New start time |
| `due_date` | datetime | No | New due time |
| `time_zone` | str | No | New time zone |
| `reminders` | List[str] | No | New reminders |
| `repeat_flag` | str | No | New recurring rules |
| `items` | List[ChecklistItem] | No | New checklist items |

### ChecklistItem

Model representing a checklist item (subtask).

#### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | str | Yes | Item title |
| `status` | int | No | Status (0=normal, 1=completed) |
| `start_date` | datetime | No | Start time |
| `is_all_day` | bool | No | All-day flag |
| `time_zone` | str | No | Time zone |

### Enums

#### TaskPriority

```python
class TaskPriority(int, Enum):
    NONE = 0    # No priority
    LOW = 1     # Low priority
    MEDIUM = 3  # Medium priority
    HIGH = 5    # High priority
```

#### TaskStatus

```python
class TaskStatus(int, Enum):
    NORMAL = 0     # Normal/incomplete
    COMPLETED = 2  # Completed
``` 