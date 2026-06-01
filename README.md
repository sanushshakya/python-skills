# User Management API

This project provides a simple CRUD API for managing users using FastAPI. The API allows you to create, read, update, and delete user records. It also includes JWT authentication for secure access.

## Features

- **User Creation**: Add new users with a unique ID, name, email, and role.
- **User Retrieval**: Fetch individual users by their ID or list all users.
- **User Update**: Modify the details of an existing user, including the role.
- **User Deletion**: Remove a user from the system.
- **Authentication**: Secure access using JWT tokens for /auth/register, /auth/login, /auth/forgot-password, and /auth/update-password endpoints.

## Updated Features

### Email Verification

The new feature includes email verification to ensure that users provide valid email addresses during registration. This is done by sending a verification token to the user's email address after successful registration. The user must then verify their email by clicking on the link in the verification email.

### Role-Based Access Control (RBAC)

Role-based access control has been implemented to allow different roles of users to have different permissions within the system. Supported roles include "user", "admin", and "superuser". Only users with appropriate roles can perform certain actions, such as deleting other users or changing user roles.

### Token Refresh

A new `/auth/refresh` endpoint has been added to refresh JWT tokens. This allows authenticated users to obtain a new access token without having to log in again after the initial token expires. The refresh token remains valid for 7 days.

## Notification System

The API now includes a real-time notification system to alert users about important events, such as changes in their profile or authentication-related actions. Notifications are sent via WebSocket and require the user to have an active connection to receive them.

### WebSocket Endpoint

A new WebSocket endpoint `/notifications` has been added to handle real-time notifications.

**Example Usage:**
```python
import websocket

ws = websocket.create_connection("ws://localhost:8000/notifications")
print("Connection established")

while True:
    message = ws.recv()
    print(f"Received notification: {message}")
```

### Notification Events

The following events can trigger notifications:

- **Profile Update**: When a user's profile is updated.
- **Login Success**: When a user successfully logs in.
- **Logout**: When a user logs out.

## Background Tasks

This project also leverages Celery and Redis for handling background tasks, such as sending email notifications. Celery acts as the task queue, while Redis serves as the message broker and cache.

### Celery Configuration

Celery is configured to use Redis as the broker and backend. You can start a Celery worker by running:

```bash
celery -A src.tasks worker --loglevel=info
```

### Email Notification Task

An email notification task has been added to send verification emails after user registration. This task runs asynchronously using Celery.

**Example Usage:**
```python
from src.tasks import send_verification_email

send_verification_email.delay(user_id, verification_token)
```

## User Profile Fields

The user profile now includes additional fields:
- **Bio**: A brief description of the user.
- **Profile Picture**: A link to the user's profile picture.
- **Date of Birth**: The user's date of birth.
- **Gender**: The user's gender (optional).

### New Endpoints

#### GET /users/me

Retrieves the current authenticated user's details.

**Response Schema:**
```json
{
  "id": int,
  "name": str,
  "email": str,
  "role": str,
  "bio": str,
  "profile_picture": str,
  "date_of_birth": str,
  "gender": str
}
```