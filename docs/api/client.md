# Client API Reference

## Dida365Client

The main client class for interacting with the Dida365/TickTick API.

### Constructor

```python
def __init__(
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    service_type: ServiceType = ServiceType.DIDA365,
    redirect_uri: str = "http://localhost:8080/callback",
    save_to_env: bool = True
)
```

Creates a new Dida365Client instance.

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `client_id` | `Optional[str]` | OAuth2 client ID. Can be set via `DIDA365_CLIENT_ID` env var | `None` |
| `client_secret` | `Optional[str]` | OAuth2 client secret. Can be set via `DIDA365_CLIENT_SECRET` env var | `None` |
| `service_type` | `ServiceType` | Service type (`DIDA365` or `TICKTICK`) | `ServiceType.DIDA365` |
| `redirect_uri` | `str` | OAuth2 redirect URI | `"http://localhost:8080/callback"` |
| `save_to_env` | `bool` | Whether to save credentials and token to `.env` file | `True` |

### Authentication Methods

#### authenticate()

```python
async def authenticate(
    scope: str = "tasks:write tasks:read",
    state: str = "state",
    port: int = 8080
) -> TokenInfo
```

Complete OAuth2 authentication flow. Opens browser for user authorization.

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `scope` | `str` | OAuth2 scopes to request | `"tasks:write tasks:read"` |
| `state` | `str` | State parameter for OAuth2 flow | `"state"` |
| `port` | `int` | Port for local callback server | `8080` |

**Returns**: `TokenInfo` - Token information including access token and expiry

#### exchange_code()

```python
async def exchange_code(code: str) -> TokenInfo
```

Exchange authorization code for access token.

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | `str` | Authorization code from OAuth2 callback |

**Returns**: `TokenInfo` - Token information including access token and expiry


### Project Methods

#### get_projects()

```python
async def get_projects() -> List[Project]
```

Get all projects.

**Returns**: `List[Project]` - List of projects

#### get_project()

```python
async def get_project(project_id: str) -> Project
```

Get a project by ID.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |

**Returns**: `Project` - Project details

#### get_project_with_data()

```python
async def get_project_with_data(project_id: str) -> ProjectData
```

Get a project with its tasks and columns.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |

**Returns**: `ProjectData` - Project details including tasks and columns

#### create_project()

```python
async def create_project(project: ProjectCreate) -> Project
```

Create a new project.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project` | `ProjectCreate` | Project creation model |

**Returns**: `Project` - Created project

#### update_project()

```python
async def update_project(project: ProjectUpdate) -> Project
```

Update an existing project.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project` | `ProjectUpdate` | Project update model |

**Returns**: `Project` - Updated project

#### delete_project()

```python
async def delete_project(project_id: str) -> None
```

Delete a project.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |

### Task Methods

#### get_task()

```python
async def get_task(project_id: str, task_id: str) -> Task
```

Get a task by project ID and task ID.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |
| `task_id` | `str` | Task identifier |

**Returns**: `Task` - Task details

#### create_task()

```python
async def create_task(task: TaskCreate) -> Task
```

Create a new task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `task` | `TaskCreate` | Task creation model |

**Returns**: `Task` - Created task

#### update_task()

```python
async def update_task(task: TaskUpdate) -> Task
```

Update an existing task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `task` | `TaskUpdate` | Task update model |

**Returns**: `Task` - Updated task

#### complete_task()

```python
async def complete_task(project_id: str, task_id: str) -> None
```

Mark a task as completed.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |
| `task_id` | `str` | Task identifier |

#### delete_task()

```python
async def delete_task(project_id: str, task_id: str) -> None
```

Delete a task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Project identifier |
| `task_id` | `str` | Task identifier |

### Error Handling

All methods can raise the following exceptions:

- `AuthenticationError`: When authentication fails or token is invalid
- `NotFoundError`: When requested resource is not found
- `ValidationError`: When request data is invalid
- `RateLimitError`: When API rate limit is exceeded
- `ApiError`: For other API errors 