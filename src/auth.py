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
    Model for user registration requests.
    """
    name: str
    email: str
    password: str

# Define a Pydantic model for the login request
class LoginRequest(BaseModel):
    """
    Model for user login requests.
    """
    email: str
    password: str

# Define a Pydantic model for the JWT token response
class TokenResponse(BaseModel):
    """
    Model for the JWT token response.
    """
    access_token: str
    token_type: str = "bearer"

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT encoding/decoding
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    """
    Verify if the plain password matches the hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.
        
    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a plain password.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    """
    Authenticate a user by email and password.
    
    Args:
        email (str): The user's email.
        password (str): The plain text password.
        
    Returns:
        dict or None: User details if authentication is successful, None otherwise.
    """
    # Here you would typically query your database to find the user by email
    fake_users_db = {
        "johndoe@example.com": {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$.eixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        }
    }
    
    user = fake_users_db.get(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.
    
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The time until the token expires. Defaults to 30 minutes.
        
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/auth/login", response_model=TokenResponse)
async def login_for_access_token(form_data: LoginRequest):
    """
    Endpoint for user login. Returns a JWT access token if credentials are valid.
    
    Args:
        form_data (LoginRequest): The login request containing email and password.
        
    Raises:
        HTTPException: If authentication fails.
        
    Returns:
        TokenResponse: The JWT access token and token type.
    """
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, token_type="bearer")