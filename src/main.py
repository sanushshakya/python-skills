from fastapi import FastAPI, HTTPException, Depends, Security, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
import logging

# Initialize FastAPI app
app = FastAPI(title="User Management API", description="A simple CRUD API for managing users.")

# In-memory database simulation using a list
users_db: List[dict] = []

# Structured logger setup with correlation ID support
logger = logging.getLogger("user_management")
logging.basicConfig(level=logging.INFO)
correlation_id_generator = lambda: str(uuid.uuid4())

@app.middleware("http")
async def add_correlation_id(request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", correlation_id_generator())
    request.state.correlation_id = correlation_id
    logger = logging.getLogger(f"user_management.{correlation_id}")
    response = await call_next(request)
    return response

# User model with additional profile fields and role is_verified fields
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    refresh_token: Optional[str] = None  # New field to store the JWT refresh token
    refresh_token_expiry: Optional[datetime] = None  # New field to store the expiry time of the JWT refresh token
    bio: Optional[str] = None  # New field for user biography
    profile_picture_url: Optional[str] = None  # New field for user profile picture URL
    social_links: Optional[List[str]] = None  # New field for list of social media links
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
        dict: The user data of the currently authenticated user if they have the requir