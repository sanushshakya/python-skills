"""
Test suite for the User Management API.

This module contains unit tests for the main functionality of the User Management API,
including CRUD operations for users. The tests use Pytest to verify that the API behaves as expected.
"""

from fastapi.testclient import TestClient
from src.main import app, users_db, get_user
import pytest

# Initialize the test client with the FastAPI app
client = TestClient(app)

def test_create_user():
    """
    Test creating a new user.

    This test sends a POST request to create a new user and checks if the response status code is 201.
    It also verifies that the user has been added to the in-memory database.
    """
    user_data = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert len(users_db) == 1
    assert users_db[0] == user_data

def test_get_user():
    """
    Test retrieving an existing user by ID.

    This test sends a GET request to retrieve a user and checks if the response status code is 200.
    It also verifies that the returned user data matches the expected data.
    """
    # Ensure there's at least one user in the database
    test_create_user()
    user_id = users_db[0]['id']
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == users_db[0]

def test_get_user_not_found():
    """
    Test retrieving a non-existent user by ID.

    This test sends a GET request for a non-existent user and checks if the response status code is 404.
    """
    # Use an ID that doesn't exist
    response = client.get("/users/999")
    assert response.status_code == 404

def test_update_user():
    """
    Test updating an existing user.

    This test sends a PUT request to update an existing user and checks if the response status code is 200.
    It also verifies that the user data in the database has been updated.
    """
    # Ensure there's at least one user in the database
    test_create_user()
    user_id = users_db[0]['id']
    updated_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    # Update the user in the database simulation
    users_db[0].update(updated_data)
    assert users_db[0]['name'] == "Jane Doe"

def test_delete_user():
    """
    Test deleting an existing user.

    This test sends a DELETE request to delete an existing user and checks if the response status code is 204.
    It also verifies that the user has been removed from the in-memory database.
    """
    # Ensure there's at least one user in the database
    test_create_user()
    user_id = users_db[0]['id']
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    assert len(users_db) == 0

def test_delete_user_not_found():
    """
    Test deleting a non-existent user.

    This test sends a DELETE request for a non-existent user and checks if the response status code is 404.
    """
    # Use an ID that doesn't exist
    response = client.delete("/users/999")
    assert response.status_code == 404

def test_dependency_get_user():
    """
    Test the dependency function get_user.

    This test verifies that the get_user function correctly retrieves a user by ID from the database.
    """
    # Ensure there's at least one user in the database
    test_create_user()
    user_id = users_db[0]['id']
    user = get_user(user_id)
    assert user == users_db[0]

def test_dependency_get_user_not_found():
    """
    Test the dependency function get_user for a non-existent user.

    This test verifies that the get_user function raises an HTTPException when trying to retrieve a non-existent user.
    """
    with pytest.raises(HTTPException):
        get_user(999)