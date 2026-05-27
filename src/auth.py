"""
Authentication module for the User Management API.

This module contains the implementation of JWT authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

router = APIRouter()

# Define a Pydantic model for the registration request
class RegisterRequest(BaseModel):
    """
    Model for user registration.
    
    Contains fields for username, email, and password.
    """
    username: str
    email: str
    password: str

# Define a Pydantic model for the login request
class LoginRequest(BaseModel):
    """
    Model for user login.
    
    Contains fields for username and password.
    """
    username: str
    password: str

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key (replace with a secure value in production)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    """
    Verify if the plain password matches the hashed password.
    
    :param plain_password: The plain text password.
    :param hashed_password: The hashed password.
    :return: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Get the hashed version of a password.
    
    :param password: The plain text password.
    :return: The hashed password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    
    :param data: Data to be encoded in the token.
    :param expires_delta: Expiration time for the token.
    :return: Encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/auth/register", response_model=dict)
async def register_user(request: RegisterRequest):
    """
    Register a new user.
    
    :param request: User registration data.
    :return: A dictionary indicating the result of the operation.
    """
    # Hash the password before storing it
    hashed_password = get_password_hash(request.password)
    
    # Here you would typically store the user in your database
    # For demonstration, we'll just return a success message
    
    return {"message": "User registered successfully", "hashed_password": hashed_password}
```

This file defines the `/auth/register` endpoint for registering new users. The `RegisterRequest` Pydantic model is used to validate incoming data, and the password is hashed using bcrypt before being stored. The `create_access_token` function is defined but not used in this snippet; it can be implemented later for user authentication.