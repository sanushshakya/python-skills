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
  "gender": str,
  "created_at": str,
  "updated_at": str
}
```

#### PUT /users/me

Updates the current authenticated user's details.

**Request Body Schema:**
```json
{
  "name": str,
  "bio": str,
  "profile_picture": str,
  "date_of_birth": str,
  "gender": str
}
```

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
  "gender": str,
  "created_at": str,
  "updated_at": str
}
```

#### File Upload Support

A new endpoint `/users/upload-avatar` has been added to allow users to upload and update their profile picture.

**Request Body Schema:**
```json
{
  "file": file
}
```

**Response Schema:**
```json
{
  "message": str,
  "profile_picture_url": str
}
```

## AI Functionalities

The API has been enhanced with AI functionalities, including chat,

=== README.md ===
# User Management API

This project provides a simple CRUD API for managing users using FastAPI. The API allows you to create, read, update, and delete user records. It also includes JWT authentication for secure access.

## Features

- **User Creation**: Add new users with a unique ID, name, email, and role.
- **User Retrieval**: Fetch individual users by their ID or list all users.
- **User Update**: Modify the details of an existing user, including the role.
- **User Deletion**: Remove a user from the system.
- **Authentication**: Secure access using JWT tokens for /auth/register, /auth/log

=== requirements.txt ===
# FastAPI
fastapi==0.85.1

# Uvicorn (for running the API)
uvicorn==0.17.6

# Pydantic for data validation
pydantic==1.9.1

# Starlette (FastAPI is built on top of Starlette)
starlette==0.19.1

# SQLAlchemy for ORM (if you plan to use a database later)
sqlalchemy==1.4.36

# Alembic for database migrations (if you plan to use a database later)
alembic==1.7.4

=== src/auth.py ===
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def generate_email_verification_token(user_id: int):
    """
    Generates a JWT token for email verification.
    
    Args:
        user_id (int): The ID of the user to be verified.

    Returns:
        str: A JWT token containing the user's ID and expiration time.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    """
    Verifies if a plain password matches its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodes a JWT token to retrieve the current authenticated user.

    Args:
        token (str): The JWT access token provided by the client.

    Returns:
        User: The current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(user_id=user_id)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Ensures that the current authenticated user is active.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current active user.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user