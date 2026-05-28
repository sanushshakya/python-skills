from fastapi import FastAPI, HTTPException, Depends, Security, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Initialize FastAPI app
app = FastAPI(title="User Management API", description="A simple CRUD API for managing users.")

# In-memory database simulation using a list
users_db: List[dict] = []

# User model with role field
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    role: str = "user"  # Default role to 'user'

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

# Dependency to get current active user
def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Retrieve the currently authenticated user.

    Args:
        token (str): The JWT token provided in the request headers.

    Returns:
        dict: The user data of the currently authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user

# Dependency to require a specific role for routes
def require_role(required_role: str):
    """
    Dependency to check if the current user has the required role.

    Args:
        required_role (str): The role required for accessing the route.

    Returns:
        dict: The user data of the currently authenticated user if they have the required role.
    """
    def inner_dependency(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return inner_dependency

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# CryptContext for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, current_user: dict = Depends(require_role("admin"))):
    """
    Create a new user.

    Args:
        user (User): The user data to be created.
        current_user (dict): The currently authenticated user, must have 'admin' role.

    Returns:
        dict: The newly created user.
    """
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {
        "id": len(users_db) + 1,
        **user.dict(),
        "hashed_password": pwd_context.hash(user.hashed_password),
    }
    users_db.append(new_user)
    return new_user

@app.get("/users", status_code=status.HTTP_200_OK, response_model=List[User])
async def read_users(current_user: dict = Depends(require_role("admin"))):
    """
    Retrieve all users.

    Args:
        current_user (dict): The currently authenticated user, must have 'admin' role.

    Returns:
        List[User]: A list of all users.
    """
    return users_db

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def read_user(user_id: int, current_user: dict = Depends(require_role("admin"))):
    """
    Retrieve a specific user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        current_user (dict): The currently authenticated user, must have 'admin' role.

    Returns:
        User: The retrieved user.
    """
    return get_user(user_id)

@app.put("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: int, user_update: User, current_user: dict = Depends(require_role("admin"))):
    """
    Update a specific user by ID.

    Args:
        user_id (int): The ID of the user to update.
        user_update (User): The updated user data.
        current_user (dict): The currently authenticated user, must have 'admin' role.

    Returns:
        User: The updated user.
    """
    if not any(u["id"] == user_id for u in users_db):
        raise HTTPException(status_code=404, detail="User not found")
    existing_user = get_user(user_id)
    updated_user = {
        **existing_user,
        **user_update.dict(),
    }
    users_db[users_db.index(existing_user)] = updated_user
    return updated_user

@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: dict = Depends(require_role("admin"))):
    """
    Delete a specific user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        current_user (dict): The currently authenticated user, must have 'admin' role.

    Returns:
        None
    """
    if not any(u["id"] == user_id for u in users_db):
        raise HTTPException(status_code=404, detail="User not found")
    users_db[:] = [u for u in users_db if u["id"] != user_id]