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

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the API)
- PyJWT for handling JWT tokens
- Passlib for password hashing
- Email library for sending verification emails

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-skills.git
   cd python-skills
   ```

2. Install the dependencies:
   ```bash
   pip install fastapi uvicorn pyjwt passlib[bcrypt] email-validator
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Usage Examples

### Create a New User

Send a POST request to `/auth/register` with user data in JSON format.

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword", "role": "user", "bio": "Software developer", "profile_picture": "https://example.com/profile.jpg", "date_of_birth": "1990-05-28", "gender": "Male"}'
```

### Login and Get JWT Token

Send a POST request to `/auth/login` with credentials in JSON format.

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"email": "john.doe@example.com", "password": "securepassword"}'
```

### Forgot Password

Send a POST request to `/auth/forgot-password` with the user's email.

```bash
curl -X POST "http://127.0.0.1:8000/auth/forgot-password" -H "Content-Type: application/json" -d '{"email": "john.doe@example.com"}'
```

### Update Password

Send a PUT request to `/auth/update-password` with the user's current password and new password.

```bash
curl -X PUT "http://127.0.0.1:8000/auth/update-password" -H "Content-Type: application/json" -d '{"current_password": "securepassword", "new_password": "new_securepassword"}'
```

### Get Current User

Send a GET request to `/users/me` with an access token.

```bash
curl -X GET "http://127.0.0.1:8000/users/me" -H "Authorization: Bearer your_access_token"
```

### Update Current User

Send a PUT request to `/users/me` with updated user data and an access token.

```bash
curl -X PUT "http://127.0.0.1:8000/users/me" -H "Content-Type: application/json" -d '{"name": "John Doe", "bio": "Updated bio"}' -H "Authorization: Bearer your_access_token"
```

### Upload Profile Picture

Send a PUT request to `/users/upload-avatar` with the profile picture file and an access token.

```bash
curl -X PUT "http://127.0.0.1:8000/users/upload-avatar" -F "file=@path/to/profile.jpg" -H "Authorization: Bearer your_access_token"
```

These updates provide a more robust user management system with additional features and endpoints.