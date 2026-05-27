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
    Model for registering a new user.
    """
    name: str
    email: str
    password: str

# Define a Pydantic model for the login request
class LoginRequest(BaseModel):
    """
    Model for user login.
    """
    email: str
    password: str

# Define a Pydantic model for the reset password request
class ResetPasswordRequest(BaseModel):
    """
    Model for resetting a user's password using a reset token.
    """
    email: str
    new_password: str
    reset_token: str

# Define a Pydantic model for the update password request
class UpdatePasswordRequest(BaseModel):
    """
    Model for updating a user's password.
    """
    current_password: str
    new_password: str

# CryptContext instance to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key (change this in production)
SECRET_KEY = "your-24-or-32-character-secret-key"
ALGORITHM = "HS256"

# Token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dummy database for users (in a real application, use a database ORM like SQLAlchemy)
fake_users_db = {
    "johndoe@example.com": {
        "id": "1",
        "name": "John Doe",
        "hashed_password": pwd_context.hash("secret"),
        "email": "johndoe@example.com"
    }
}

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with the given data and expiration time.

    Args:
        data (dict): Data to be encoded in the token.
        expires_delta (timedelta, optional): Expiration time for the token. Defaults to None.

    Returns:
        str: The created JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify a JWT token
def verify_token(token: str):
    """
    Verify the given JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: Decoded data from the token if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Function to authenticate a user and return an access token
def authenticate_user(email: str, password: str):
    """
    Authenticate a user by email and password.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        dict: User data if authentication is successful, None otherwise.
    """
    user = fake_users_db.get(email)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return None
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    user.update({"access_token": access_token})
    return user

# Function to reset a user's password using a reset token
def reset_password(email: str, new_password: str, reset_token: str):
    """
    Reset a user's password using a reset token.

    Args:
        email (str): The user's email.
        new_password (str): The new password for the user.
        reset_token (str): The reset token provided by the user.

    Returns:
        bool: True if the password was successfully updated, False otherwise.
    """
    user = fake_users_db.get(email)
    if not user or not verify_reset_token(user["reset_token"], reset_token):
        return False
    user["hashed_password"] = pwd_context.hash(new_password)
    return True

# Function to update a user's password using the current and new passwords
def update_password(current_password: str, new_password: str, email: str):
    """
    Update a user's password using the current and new passwords.

    Args:
        current_password (str): The user's current password.
        new_password (str): The user's new password.
        email (str): The user's email.

    Returns:
        bool: True if the password was successfully updated, False otherwise.
    """
    user = fake_users_db.get(email)
    if not user or not pwd_context.verify(current_password, user["hashed_password"]):
        return False
    user["hashed_password"] = pwd_context.hash(new_password)
    return True

# Function to verify a reset token
def verify_reset_token(token: str, expected_email: str):
    """
    Verify the given reset token against an expected email.

    Args:
        token (str): The reset token to verify.
        expected_email (str): The expected email associated with the token.

    Returns:
        bool: True if the token is valid and matches the expected email, False otherwise.
    """
    payload = verify_token(token)
    if not payload or payload["sub"] != expected_email:
        return False
    return True

# /auth/register endpoint to register a new user
@router.post("/register")
async def register_user(user: RegisterRequest):
    """
    Register a new user.

    Args:
        user (RegisterRequest): The user data to register.

    Returns:
        dict: A message indicating successful registration.
    """
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    reset_token = create_access_token(data={"sub": user.email}, expires_delta=None)
    fake_users_db[user.email] = {
        "id": str(len(fake_users_db) + 1),
        "name": user.name,
        "hashed_password": hashed_password,
        "email": user.email,
        "reset_token": reset_token
    }
    return {"message": "User registered successfully"}

# /auth/login endpoint to authenticate a user and return an access token
@router.post("/login")
async def login_user(user: LoginRequest):
    """
    Authenticate a user and return an access token.

    Args:
        user (LoginRequest): The user data for authentication.

    Returns:
        dict: The user data with an access token.
    """
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return authenticated_user

# /auth/forgot-password endpoint to request a password reset
@router.post("/forgot-password")
async def forgot_password(user: ResetPasswordRequest):
    """
    Request a password reset for the given email.

    Args:
        user (ResetPasswordRequest): The user data for requesting a password reset.

    Returns:
        dict: A message indicating that a password reset has been requested.
    """
    if user.email not in fake_users_db:
        raise HTTPException(status_code=400, detail="Email not found")
    # In a real application, you would send an email with the reset token
    return {"message": "Password reset requested. Check your email for instructions."}

# /auth/update-password endpoint to update a user's password using the current and new passwords
@router.post("/update-password")
async def update_user_password(user: UpdatePasswordRequest):
    """
    Update a user's password using the current and new passwords.

    Args:
        user (UpdatePasswordRequest): The user data for updating the password.

    Returns:
        dict: A message indicating that the password has been updated.
    """
    if not update_password(user.current_password, user.new_password, user.email):
        raise HTTPException(status_code=400, detail="Invalid current password")
    return {"message": "Password updated successfully"}