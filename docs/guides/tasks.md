# Working with Tasks

This guide covers all task-related operations available in the API client.

## Task Models

### TaskCreate


Used when creating a new task:

```python
from datetime import datetime, timezone
from dida365 import TaskCreate, TaskPriority

task = TaskCreate(
    project_id="project_id",       # Required: Project ID, "" for inbox
    title="My Task",               # Required: Task title
    content="Task details",        # Optional: Task content
    desc="Task description",       # Optional: Task description
    priority=TaskPriority.HIGH,    # Optional: Task priority
    is_all_day=False,             # Optional: All-day task
    start_date=datetime.now(timezone.utc),  # Optional: Start time
    due_date=None,                # Optional: Due time
    time_zone="UTC",              # Optional: Time zone
    reminders=["TRIGGER:PT0S"],   # Optional: Reminder triggers
    repeat_flag=None,             # Optional: Recurring rules
    items=[                       # Optional: Checklist items
        {
            "title": "Subtask 1",
            "status": 0
        }
    ]
)
```

!!! note
    If the provided `project_id` does not exist, the task will be created in the inbox. You can also explicitly create a task in the inbox by setting `project_id=""` (empty string).





### TaskUpdate
Used when updating an existing task:

```python
from dida365 import TaskUpdate, TaskPriority

update = TaskUpdate(
    id="task_id",                 # Required: Task ID
    project_id="project_id",      # Required: Project ID
    title="Updated Task",         # Optional: New title
    priority=TaskPriority.MEDIUM  # Optional: New priority
)
```

## Basic Operations

### Create a Task

```python
# Simple task
task = await client.create_task(
    TaskCreate(
        project_id="project_id",
        title="Simple Task"
    )
)

# Detailed task
from datetime import datetime, timezone
task = await client.create_task(
    TaskCreate(
        project_id="project_id",
        title="Important Meeting",
        content="Quarterly review",
        priority=TaskPriority.HIGH,
        start_date=datetime.now(timezone.utc),
        is_all_day=False,
        time_zone="UTC",
        reminders=["TRIGGER:PT0S"],  # Reminder at start time
        items=[
            {"title": "Prepare slides", "status": 0},
            {"title": "Review metrics", "status": 0}
        ]
    )
)
```

### Get Tasks

```python
# Get a specific task
task = await client.get_task("project_id", "task_id")

# Get all tasks in a project
project_data = await client.get_project_with_data("project_id")
tasks = project_data.tasks
```

### Update a Task

```python
# Update specific fields
updated = await client.update_task(
    TaskUpdate(
        id="task_id",
        project_id="project_id",
        title="New Title"
    )
)

# Full update
updated = await client.update_task(
    TaskUpdate(
        id="task_id",
        project_id="project_id",
        title="Updated Task",
        content="New content",
        priority=TaskPriority.HIGH,
        start_date=datetime.now(timezone.utc),
        items=[
            {"title": "New subtask", "status": 0}
        ]
    )
)
```

### Complete/Delete Tasks

```python
# Mark task as complete
await client.complete_task("project_id", "task_id")

# Delete task
await client.delete_task("project_id", "task_id")
```

## Task Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | str | Yes (update) | Task identifier |
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
| `items` | List[dict] | No | Checklist items |
| `status` | TaskStatus | No | Task status |

## Priority Levels

```python
from dida365 import TaskPriority

# Available priority levels:
TaskPriority.NONE    # No priority (0)
TaskPriority.LOW     # Low priority (1)
TaskPriority.MEDIUM  # Medium priority (3)
TaskPriority.HIGH    # High priority (5)
```

## Task Status

```python
from dida365 import TaskStatus

# Available status values:
TaskStatus.NORMAL     # Normal/incomplete (0)
TaskStatus.COMPLETED  # Completed (2)
```

## Checklist Items

Checklist items (subtasks) have their own properties:

```python
checklist_item = {
    "title": "Subtask",           # Required: Item title
    "status": 0,                  # Optional: 0=normal, 1=completed
    "start_date": datetime.now(), # Optional: Start time
    "is_all_day": False,         # Optional: All-day item
    "time_zone": "UTC"           # Optional: Time zone
}
```

## Error Handling

```python
from dida365.exceptions import NotFoundError, ValidationError

try:
    task = await client.get_task("project_id", "non_existent_id")
except NotFoundError:
    print("Task not found")
except ValidationError as e:
    print(f"Invalid data: {e}")
```

## Complete Example

```python
from datetime import datetime, timezone
from dida365 import (
    Dida365Client,
    TaskCreate,
    TaskUpdate,
    TaskPriority,
    ProjectCreate
)

async def manage_tasks():
    client = Dida365Client()
    
    # Create a project first
    project = await client.create_project(
        ProjectCreate(name="Task Demo")
    )
    
    # Create a task with subtasks
    task = await client.create_task(
        TaskCreate(
            project_id=project.id,
            title="Important Task",
            content="Task details",
            priority=TaskPriority.HIGH,
            start_date=datetime.now(timezone.utc),
            items=[
                {"title": "Subtask 1", "status": 0},
                {"title": "Subtask 2", "status": 0}
            ]
        )
    )
    
    # Update the task
    updated = await client.update_task(
        TaskUpdate(
            id=task.id,
            project_id=project.id,
            title="Updated Task",
            priority=TaskPriority.MEDIUM
        )
    )
    
    # Mark as complete
    await client.complete_task(project.id, task.id)
    
    # Clean up
    await client.delete_task(project.id, task.id)
    await client.delete_project(project.id)
``` 