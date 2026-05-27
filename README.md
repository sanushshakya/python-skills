# User Management API

This project provides a simple CRUD API for managing users using FastAPI. The API allows you to create, read, update, and delete user records. It also includes JWT authentication for secure access.

## Features

- **User Creation**: Add new users with a unique ID, name, and email.
- **User Retrieval**: Fetch individual users by their ID or list all users.
- **User Update**: Modify the details of an existing user.
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
curl -X POST "http://127.0.0.1:8000/auth/register" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com", "password": "securepassword"}'
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
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -H "Authorization: Bearer <jwt_token>" -d '{"name": "Jane Doe", "email": "jane.doe@example.com"}'
```

## Project Structure

```
python-skills/
│
├── README.md
├── src/
│   ├── config.py       # Configuration settings for the API
│   ├── main.py         # Main application logic and routes
│   ├── models.py     # User model with hashed_password and reset_token fields
│   └── utils.py        # Utility functions including JWT handling
└── tests/
    └── test_main.py  # Test suite for the API
```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.