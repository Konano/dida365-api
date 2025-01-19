# Authentication Guide

This guide explains how to set up authentication for the Dida365/TickTick API client.

## Prerequisites

Before you start, you'll need:

1. A TickTick or Dida365 account
2. Access to the developer portal:
    - TickTick: <https://developer.ticktick.com/manage>
    - Dida365: <https://developer.dida365.com/manage>

## Step 1: Create an Application

1. Visit the appropriate developer portal (TickTick or Dida365)
2. Click "New App" to create a new application
3. Fill in the required information
4. After creation, you'll receive:
    - Client ID
    - Client Secret

## Step 2: Configure OAuth2 Redirect URL

1. In your app's settings, click "Edit"
2. Add the redirect URL: `http://localhost:8080/callback`
3. Save the changes

!!! note
    If you want to use a different redirect URL, make sure to update it both in the developer portal and when initializing the client.

## Step 3: Configure Credentials

You have two options for configuring credentials:

### Option 1: Environment Variables (Recommended)

Create a `.env` file in your project root:
```bash
DIDA365_CLIENT_ID=your_client_id
DIDA365_CLIENT_SECRET=your_client_secret
DIDA365_SERVICE_TYPE=ticktick  # or dida365
DIDA365_REDIRECT_URI=http://localhost:8080/callback  # Optional
```

Then initialize the client:
```python
from dida365 import Dida365Client

client = Dida365Client()  # Will load from .env
```

### Option 2: Direct Configuration

Pass credentials directly when initializing the client:
```python
from dida365 import Dida365Client, ServiceType

client = Dida365Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    service_type=ServiceType.TICKTICK,  # or DIDA365
    redirect_uri="http://localhost:8080/callback",  # Optional
    save_to_env=True  # Save credentials to .env file
)
```

## Step 4: Authentication Flow

The first time you use the client, you need to authenticate:

```python
# This will open your browser for authorization
token_info = await client.authenticate()

# The token will be automatically saved if save_to_env=True
# For subsequent runs, the token will be loaded automatically
```

### Token Management

- If `save_to_env=True`, tokens are saved to your `.env` file

## Configuration Options

| Parameter       | Required | Default                            | Description                         |
| --------------- | -------- | ---------------------------------- | ----------------------------------- |
| `client_id`     | Yes      | None                               | OAuth2 client ID                    |
| `client_secret` | Yes      | None                               | OAuth2 client secret                |
| `service_type`  | No       | `ServiceType.DIDA365`              | Service type (TICKTICK or DIDA365)  |
| `redirect_uri`  | No       | `"http://localhost:8080/callback"` | OAuth2 redirect URI                 |
| `save_to_env`   | No       | `True`                             | Save credentials and tokens to .env |

## Error Handling

```python
from dida365.exceptions import AuthenticationError

try:
    await client.authenticate()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## Common authentication errors problems shooting:
    
  - Invalid client credentials 
      - check you have the correct service type (ServiceType.TICKTICK or ServiceType.DIDA365)
      - correctness of client ID/secret
  - Invalid redirect URI 
      - by default, the client will use `http://localhost:8080/callback`
      - check you have set the correct redirect URI in the developer portal 
      -  .env or when initializing the client if you using alternative redirect URI
  - User denied access (check the browser)
  - Network connectivity issues (check your internet connection)