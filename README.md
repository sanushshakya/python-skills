# User Management API

This project provides a simple CRUD API for managing users using FastAPI. The API allows you to create, read, update, and delete user records. It also includes JWT authentication for secure access.

## Features

- **User Creation**: Add new users with a unique ID, name, email, and role.
- **User Retrieval**: Fetch individual users by their ID or list all users.
- **User Update**: Modify the details of an existing user, including the role.
- **User Deletion**: Remove a user from the system.
- **Authentication**: Secure access using JWT tokens for /auth/register, /auth/login, /auth/forgot-password, and /auth/update-password endpoints.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the API)
- PyJWT for handling JWT tokens
- Passlib for password hashing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-skills.git
   cd python-skills
   ```

2. Install the dependencies:
   ```bash
   pip install fastapi uvicorn pyjwt passlib[bcrypt]
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

### Create a New User (Authenticated)

Send a POST request to `/users/` with user data in JSON format and include the JWT token in the Authorization header.

```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{"name": "Jane Doe", "email": "jane.doe@example.com", "role": "user"}'
```

## Project Structure

```
python-skills/
│
├── README.md
├── src/
│   ├── config.py       # Configuration settings for the API
│   ├── main.py         # Main application logic and routes
│   ├── models.py     # User model with hashed_password, reset_token, and role fields
│   └── utils.py        # Utility functions including JWT handling
└── tests/
    └── tes
```

## Updated Features

### Role Field in User Model

The `User` model now includes a `role` field to specify the user's role. This field can be one of "user", "admin", or any other role defined by your application.

### Require Role Dependency

A new dependency, `require_role`, is introduced to restrict access to certain routes based on the user's role. For example, only users with the "admin" role can create, update, and delete users.

### Restricted CRUD Routes

- **Create User**: Only accessible to users with the "admin" role.
- **Update User**: Only accessible to users with the "admin" role or the user themselves.
- **Delete User**: Only accessible to users with the "admin" role or the user themselves.

These changes ensure that your API adheres to a more robust security model, where roles dictate access to specific functionalities. This aligns with best practices for managing user privileges in web applications.