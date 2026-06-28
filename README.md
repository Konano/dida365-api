# dida365-api

An unofficial Python client library for the Dida365/TickTick API, supporting both the Chinese (Dida365) and international (TickTick) versions of the service. Built with modern async Python and robust error handling.

> **Forked from** [Cyfine/TickTick-Dida365-API-Client](https://github.com/Cyfine/TickTick-Dida365-API-Client) — thanks to [Carter Yifeng Cheng (@cyfine)](https://github.com/cyfine) for the original project.

This is a community package created to facilitate task management automation. It is not affiliated with or endorsed by Dida365 or TickTick.

## Installation

```bash
pip install dida365-api
```

To install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/Konano/dida365-api.git
```

## Quick Start

```python
import asyncio
from dida365 import Dida365Client, ServiceType, TaskCreate, TaskPriority

async def main():
    # Credentials can be passed via constructor, .env file, or environment variables
    client = Dida365Client(
        client_id="your_client_id",
        client_secret="your_client_secret",
        service_type=ServiceType.TICKTICK,  # or ServiceType.DIDA365
        redirect_uri="http://localhost:8080/callback",
        save_to_env=True,  # automatically save credentials & tokens to .env
        # access_token="your_access_token",  # If you already have an access_token, pass it directly to skip OAuth
    )

    # First-time authentication (opens browser, starts local callback server)
    if not client.auth.token:
        await client.authenticate()

    # Create a task
    task = await client.create_task(
        TaskCreate(
            project_id="your_project_id",
            title="My new task",
            content="Task description",
            priority=TaskPriority.HIGH,
        )
    )
    print(f"Created task: {task.title}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

Credentials can be provided in three ways (checked in this order):

1. **Constructor parameters** — directly pass `client_id`, `client_secret`, `access_token`, etc.
2. **`.env` file** — create a `.env` in your working directory
3. **Environment variables**

Example `.env` file:

```bash
DIDA365_CLIENT_ID=your_client_id
DIDA365_CLIENT_SECRET=your_client_secret
DIDA365_REDIRECT_URI=http://localhost:8080/callback
DIDA365_SERVICE_TYPE=ticktick  # or dida365
DIDA365_ACCESS_TOKEN=your_token  # optional: set to skip OAuth flow
```

### OAuth2 Setup

1. Get your credentials:
   - TickTick: https://developer.ticktick.com/manage
   - Dida365: https://developer.dida365.com/manage
   - Click **New App**, then note your Client ID and Client Secret.
2. In your app's settings, add the redirect URL: `http://localhost:8080/callback`

## API Reference

Official documentation:
- Dida365 API: https://developer.dida365.com/api#/openapi
- TickTick API: https://developer.ticktick.com/docs#/openapi

## Usage

### Tasks

```python
from dida365 import TaskCreate, TaskUpdate, TaskPriority, TaskStatus

# Create
task = await client.create_task(
    TaskCreate(
        project_id="project_id",
        title="Complete documentation",
        priority=TaskPriority.HIGH,
    )
)

# Read
task = await client.get_task(project_id="project_id", task_id=task.id)

# Update
task = await client.update_task(
    TaskUpdate(
        id=task.id,
        project_id=task.project_id,
        title="Updated title",
    )
)

# Complete
await client.complete_task(project_id=task.project_id, task_id=task.id)

# Delete
await client.delete_task(project_id=task.project_id, task_id=task.id)

# Filter tasks
tasks = await client.filter_tasks(
    project_ids=["project_id"],
    priority=[TaskPriority.HIGH],
    status=[TaskStatus.NORMAL],
)
```

### Projects

```python
from dida365 import ProjectCreate, ProjectUpdate, ViewMode

# Create
project = await client.create_project(
    ProjectCreate(name="My Project", color="#FF0000", view_mode=ViewMode.KANBAN)
)

# List all
projects = await client.get_projects()

# Get with tasks & columns
data = await client.get_project_with_data(project_id=project.id)

# Update
project = await client.update_project(
    ProjectUpdate(id=project.id, name="Renamed Project")
)

# Delete
await client.delete_project(project_id=project.id)
```

### Tags

```python
from dida365 import TagCreate

# List tags
tags = await client.get_tags()

# Create a tag
tag = await client.create_tag(TagCreate(name="urgent", label="urgent"))
```

### Habits

```python
from dida365 import HabitCreate, HabitUpdate

# List all habits
habits = await client.get_all_habits()

# Create a habit
habit = await client.create_habit(
    HabitCreate(name="Morning run", color="#00FF00", sort_order=0)
)

# Update a habit
habit = await client.update_habit(habit_id=habit.id, habit=HabitUpdate(name="Evening run"))

# Get habit checkins
checkins = await client.get_habit_checkins(
    habit_ids=habit.id, from_stamp=20240101, to_stamp=20240131
)
```

### Focus

```python
from datetime import datetime, timezone, timedelta
from dida365 import FocusCreate, FocusType

# Get focus sessions
sessions = await client.get_focuses(
    from_date="2024-01-01T00:00:00+0800",
    to_date="2024-01-31T00:00:00+0800",
    focus_type=FocusType.POMODORO,
)

# Create a focus session
focus = await client.create_focus(
    FocusCreate(
        type=FocusType.POMODORO,
        start_time=datetime(2024, 1, 1, 9, 0, 0, tzinfo=timezone(timedelta(hours=8))),
        end_time=datetime(2024, 1, 1, 9, 25, 0, tzinfo=timezone(timedelta(hours=8))),
        duration=1500,
    )
)
```

### Countdown

```python
# List all countdowns
countdowns = await client.get_countdowns()
```

## Requirements

- Python 3.10 or higher

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

Original project by [Carter Yifeng Cheng (@cyfine)](https://github.com/cyfine).  
This fork maintained by [Konano](https://github.com/Konano).
