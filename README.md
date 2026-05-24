# User Management API

This project provides a simple CRUD API for managing users using FastAPI. The API allows you to create, read, update, and delete user records.

## Features

- **User Creation**: Add new users with a unique ID, name, and email.
- **User Retrieval**: Fetch individual users by their ID or list all users.
- **User Update**: Modify the details of an existing user.
- **User Deletion**: Remove a user from the system.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the API)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-skills.git
   cd python-skills
   ```

2. Install the dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Usage Examples

### Create a New User

Send a POST request to `/users/` with user data in JSON format.

```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john.doe@example.com"}'
```

### Retrieve a User

Send a GET request to `/users/{user_id}` to fetch a specific user.

```bash
curl http://127.0.0.1:8000/users/1
```

### Update a User

Send a PUT request to `/users/{user_id}` with updated user data in JSON format.

```bash
curl -X PUT "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"name": "Jane Doe", "email": "jane.doe@example.com"}'
```

### Delete a User

Send a DELETE request to `/users/{user_id}` to remove a user.

```bash
curl -X DELETE http://127.0.0.1:8000/users/1
```

## Project Structure

```
python-skills/
│
├── README.md
├── src/
│   ├── config.py       # Configuration settings for the API
│   ├── main.py         # Main application logic and routes
│   └── utils.py        # Utility functions
└── tests/
    └── test_main.py  # Test suite for the API
```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.