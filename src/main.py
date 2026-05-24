from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List

# Initialize FastAPI app
app = FastAPI(title="User Management API", description="A simple CRUD API for managing users.")

# In-memory database simulation using a list
users_db: List[dict] = []

# User model
class User(BaseModel):
    id: int
    name: str
    email: EmailStr

# Dependency to fetch user by ID
def get_user(user_id: int) -> dict:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user data if found.

    Raises:
        HTTPException: If the user is not found.
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to create a new user
@app.post("/users/", response_model=User)
def create_user(user: User):
    """
    Create a new user.

    Args:
        user (User): The user data to be created.

    Returns:
        User: The created user data.
    """
    users_db.append(user.dict())
    return user

# Endpoint to read all users
@app.get("/users/", response_model=List[User])
def read_users():
    """
    Retrieve a list of all users.

    Returns:
        List[User]: A list of user data.
    """
    return users_db

# Endpoint to read a single user by ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user: dict = Depends(get_user)):
    """
    Retrieve a user by their ID.

    Args:
        user (dict): The user data retrieved from the dependency.

    Returns:
        User: The user data.
    """
    return user

# Endpoint to update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, new_user_data: User):
    """
    Update an existing user's data.

    Args:
        user_id (int): The ID of the user to update.
        new_user_data (User): The new data for the user.

    Returns:
        User: The updated user data.

    Raises:
        HTTPException: If the user is not found.
    """
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db[i] = new_user_data.dict()
            return new_user_data
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user: dict = Depends(get_user)):
    """
    Delete a user by their ID.

    Args:
        user (dict): The user data retrieved from the dependency.

    Returns:
        User: The deleted user data.
    """
    users_db.remove(user)
    return user