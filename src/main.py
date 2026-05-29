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

# User model with role and is_verified fields
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    refresh_token: Optional[str] = None  # New field to store the JWT refresh token
    refresh_token_expiry: Optional[datetime] = None  # New field to store the expiry time of the JWT refresh token
    role: str = "user"  # Default role to 'user'
    is_verified: bool = False  # New field to indicate if the user's email is verified

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

# Initialize FastAPI app
app = FastAPI(title="User Management API", description="A simple CRUD API for managing users.")

# In-memory database simulation using a list
users_db: List[dict] = []

# User model with role and is_verified fields
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    refresh_token: Optional[str] = None  # New field to store the JWT refresh token
    refresh_token_expiry: Optional[datetime] = None  # New field to store the expiry time of the JWT refresh token
    role: str = "user"  # Default role to 'user'
    is_verified: bool = False  # New field to indicate if the user's email is verified

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

# Function to verify a password
def verify_password(plain_password, hashed_password):
    """
    Verify if the plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a password
def get_password_hash(password):
    """
    Generate and return the hashed version of the given password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)