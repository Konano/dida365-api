# Exceptions API Reference

## Base Exception

### ApiError

Base exception class for all API-related errors.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `message` | str | Error message |
| `error_code` | Optional[str] | Error code from API |
| `error_id` | Optional[str] | Error ID from API |

## Specific Exceptions

### AuthenticationError

Raised when authentication fails or token is invalid.

Example:
```python
try:
    await client.authenticate()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

Common causes:
- Invalid client credentials
- Invalid or expired token
- Missing required scopes
- User denied access

### NotFoundError

Raised when requested resource is not found.

Example:
```python
try:
    task = await client.get_task("project_id", "non_existent_id")
except NotFoundError as e:
    print(f"Task not found: {e}")
```

Common causes:
- Invalid project ID
- Invalid task ID
- Resource was deleted

### ValidationError

Raised when request data is invalid.

Example:
```python
try:
    await client.create_task(TaskCreate(project_id="", title=""))
except ValidationError as e:
    print(f"Invalid data: {e}")
```

Common causes:
- Missing required fields
- Invalid field values
- Invalid data types
- Invalid URL format

### RateLimitError

Raised when API rate limit is exceeded.

Example:
```python
try:
    tasks = await client.get_tasks()
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
```

Common causes:
- Too many requests in short time
- Exceeded API quota
- Need to implement rate limiting or backoff 