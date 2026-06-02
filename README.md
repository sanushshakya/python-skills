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

An email notification task has been added to send verification emails after user registration.

## New Features

### Structured Logging with Correlation IDs

The project now uses structured logging with correlation IDs to help trace requests through the system. This allows for better monitoring and debugging.

### Prometheus Metrics Endpoint

A new `/metrics` endpoint has been added to provide metrics about the API's performance using Prometheus.

### OpenTelemetry Tracing for Database Queries

OpenTelemetry tracing has been integrated into the database queries to provide visibility into query performance and help identify bottlenecks.

### Health Endpoints

Health endpoints have been created to check the status of various components, such as the database connection and Redis. This helps ensure that the API is running smoothly and can quickly identify any issues.

## Conclusion

These new features and improvements make the User Management API more robust, secure, and efficient. By leveraging structured logging, Prometheus metrics, OpenTelemetry tracing, and health endpoints, developers can gain deeper insights into their application's performance and reliability.