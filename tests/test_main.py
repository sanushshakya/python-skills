import pytest
from fastapi.testclient import TestClient
from src.main import app, get_current_user, User, Role
from sqlalchemy.orm import Session

# Test client to interact with the API
client = TestClient(app)

# Fixture to create a test user and role in the database
@pytest.fixture(scope="module")
def db_user_role(db: Session):
    # Create a new role for testing
    role = Role(name="admin")
    db.add(role)
    db.commit()
    db.refresh(role)

    # Create a new user with the admin role
    test_user = User(
        name="testuser",
        email="testuser@example.com",
        password="password123",
        role_id=role.id
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    yield test_user

# Test case to ensure only users with the correct role can perform CRUD operations
def test_crud_operations_with_role(db_user_role: User, db: Session):
    # Attempt to create a new user without a JWT token (should fail)
    response = client.post("/users/", json={"name": "newuser", "email": "newuser@example.com", "password": "password123"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    # Authenticate with a JWT token (use the test user's role)
    login_data = {
        "username": db_user_role.email,
        "password": "password123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    access_token = response.json().get("access_token")

    # Create a new user with the JWT token (should succeed)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users/", json={"name": "newuser", "email": "newuser@example.com", "password": "password123"}, headers=headers)
    assert response.status_code == 201
    new_user_id = response.json().get("id")

    # Retrieve the newly created user (should succeed)
    response = client.get(f"/users/{new_user_id}", headers=headers)
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["name"] == "newuser"
    assert retrieved_user["email"] == "newuser@example.com"

    # Update the newly created user (should succeed)
    update_data = {"name": "updateduser", "email": "updateduser@example.com"}
    response = client.put(f"/users/{new_user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "updateduser"
    assert updated_user["email"] == "updateduser@example.com"

    # Delete the newly created user (should succeed)
    response = client.delete(f"/users/{new_user_id}", headers=headers)
    assert response.status_code == 204

# Test case to ensure that users without the correct role cannot perform CRUD operations
def test_crud_operations_without_role(db: Session):
    # Create a new user with a different role (e.g., "user")
    role = Role(name="user")
    db.add(role)
    db.commit()
    db.refresh(role)

    test_user = User(
        name="testuser2",
        email="testuser2@example.com",
        password="password123",
        role_id=role.id
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # Authenticate with a JWT token (use the test user's role)
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    access_token = response.json().get("access_token")

    # Attempt to create a new user with the JWT token (should fail due to role restriction)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users/", json={"name": "newuser", "email": "newuser@example.com", "password": "password123"}, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Insufficient permissions"}

# Test case to ensure that the role dependency is working correctly
def test_role_dependency(db_user_role: User, db: Session):
    # Authenticate with a JWT token (use the test user's role)
    login_data = {
        "username": db_user_role.email,
        "password": "password123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    access_token = response.json().get("access_token")

    # Call a protected endpoint with the JWT token (should succeed)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}

# Test case to ensure that users without the correct role cannot access protected endpoints
def test_protected_endpoint_without_role(db: Session):
    # Create a new user with a different role (e.g., "user")
    role = Role(name="user")
    db.add(role)
    db.commit()
    db.refresh(role)

    test_user = User(
        name="testuser2",
        email="testuser2@example.com",
        password="password123",
        role_id=role.id
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # Authenticate with a JWT token (use the test user's role)
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    access_token = response.json().get("access_token")

    # Call a protected endpoint with the JWT token (should fail due to role restriction)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Insufficient permissions"}