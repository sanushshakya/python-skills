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

The API has been enhanced with AI functionalities, including chat, summarization, and smart search.

### AI Endpoints

#### POST /chat

Provides real-time chat functionality between users and an AI assistant.

**Request Body Schema:**
```json
{
  "message": str,
  "user_id": int
}
```

**Response Schema:**
```json
{
  "response": str
}
```

#### POST /summarize

Summarizes a given text using AI technology.

**Request Body Schema:**
```json
{
  "text": str
}
```

**Response Schema:**
```json
{
  "summary": str
}
```

#### POST /search

Performs smart search based on user queries and returns relevant results.

**Request Body Schema:**
```json
{
  "query": str
}
```

**Response Schema:**
```json
{
  "results": list
}
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the API)
- PyJWT for handling JWT tokens
- pydantic for data validation
- starlette (FastAPI is built on top of Starlette)
- sqlalchemy for ORM (if you plan to use a database later)
- alembic for database migrations (if you plan to use a database later)