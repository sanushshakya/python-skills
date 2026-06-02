from fastapi import FastAPI, HTTPException, Depends, Security, status, Request
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
import logging
from prometheus_client import start_http_server, Counter, Gauge
import time

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

# Prometheus metrics setup
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Gauge('http_request_latency_seconds', 'HTTP request latency in seconds')

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    REQUEST_COUNT.labels(status=exc.status_code).inc()
    return await exc.state.http_exception_handler(request, exc)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_COUNT.labels(status=response.status_code).inc()
    REQUEST_LATENCY.set(process_time)
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
def get_current_user(user_id: int = Depends(get_user)):
    """
    Get the current active user based on their ID.

    Args:
        user_id (int): The ID of the current user.

    Returns:
        dict: The current user's data.
    """
    return user

# Health endpoint to check if the application is up
@app.get("/health")
async def health():
    """
    Check the overall status of the application.

    Returns:
        dict: A dictionary indicating that the application is healthy.
    """
    return {"status": "healthy"}

# Detailed health endpoint to provide more information about the application's status
@app.get("/health/detailed")
async def health_detailed():
    """
    Provide detailed information about the application's status, including database connection and service availability.

    Returns:
        dict: A dictionary with detailed health information.
    """
    # Add logic here to check additional health metrics such as database connectivity
    return {"status": "healthy", "database": {"connected": True}, "services": {"available": ["auth", "db"]}}