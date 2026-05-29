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
curl -X POST "http://127.0.0.1:8000/auth/register" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword", "role": "user"}'
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

Send a PUT request to `/auth/update-password` with the user's email and new password.

```bash
curl -X PUT "http://127.0.0.1:8000/auth/update-password" -H "Content-Type: application/json" -d '{"email": "john.doe@example.com", "new_password": "newsecurepassword"}'
```

### Refresh JWT Token

Send a POST request to `/auth/refresh` with the user's refresh token.

```bash
curl -X POST "http://127.0.0.1:8000/auth/refresh" -H "Content-Type: application/json" -d '{"refresh_token": "your_refresh_token_here"}'
```

## Endpoints

### `/auth/register`

**Method**: POST  
**Description**: Register a new user.  
**Request Body**: JSON  
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword",
  "role": "user"
}
```
**Response**:
- **201 Created**: User registered successfully.
- **400 Bad Request**: Invalid input.

### `/auth/login`

**Method**: POST  
**Description**: Authenticate a user and return JWT tokens.  
**Request Body**: JSON  
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```
**Response**:
- **200 OK**: Authentication successful.
- **401 Unauthorized**: Invalid credentials.

### `/auth/forgot-password`

**Method**: POST  
**Description**: Send a password reset email.  
**Request Body**: JSON  
```json
{
  "email": "john.doe@example.com"
}
```
**Response**:
- **200 OK**: Email sent successfully.
- **404 Not Found**: User not found.

### `/auth/update-password`

**Method**: PUT  
**Description**: Update a user's password.  
**Request Body**: JSON  
```json
{
  "email": "john.doe@example.com",
  "new_password": "newsecurepassword"
}
```
**Response**:
- **200 OK**: Password updated successfully.
- **401 Unauthorized**: Invalid credentials.

### `/auth/refresh`

**Method**: POST  
**Description**: Refresh a JWT access token using the refresh token.  
**Request Body**: JSON  
```json
{
  "refresh_token": "your_refresh_token_here"
}
```
**Response**:
- **200 OK**: New access token.
- **401 Unauthorized**: Invalid refresh token.

These endpoints provide a comprehensive set of tools for managing user authentication and authorization within the API.