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


# Define a Pydantic model for the forgot password request
class ForgotPasswordRequest(BaseModel):
    """
    Model for requesting a password reset.
    """
    email: str


# Define a Pydantic model for the update password request
class UpdatePasswordRequest(BaseModel):
    """
    Model for updating a user's password.
    """
    reset_token: str
    new_password: str


# Initialize a CryptContext for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    """
    Verify if a plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generate a hashed version of the password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode a JWT access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Dummy user database for demonstration purposes
users_db = {
    "user@example.com": {
        "id": 1,
        "name": "John Doe",
        "hashed_password": get_password_hash("secret"),
        "reset_token": None,
    }
}


@router.post("/auth/register", response_model=dict)
async def register(user: RegisterRequest):
    """
    Endpoint to register a new user.
    """
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)
    users_db[user.email] = {
        "id": len(users_db) + 1,
        "name": user.name,
        "hashed_password": hashed_password,
        "reset_token": None,
    }
    return {"message": "User registered successfully"}


@router.post("/auth/login", response_model=dict)
async def login(user: LoginRequest):
    """
    Endpoint to log in a user and return an access token.
    """
    if user.email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not registered"
        )
    stored_user = users_db[user.email]
    if not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/forgot-password", response_model=dict)
async def forgot_password(user: ForgotPasswordRequest):
    """
    Endpoint to request a password reset.
    """
    if user.email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not registered"
        )
    stored_user = users_db[user.email]
    # In a real application, you would generate and send an email with the reset token
    reset_token = "your-reset-token-here"
    stored_user["reset_token"] = reset_token
    return {"message": f"Password reset token sent to {user.email}"}


@router.post("/auth/update-password", response_model=dict)
async def update_password(user: UpdatePasswordRequest):
    """
    Endpoint to update a user's password using a reset token.
    """
    if user.reset_token not in users_db.values():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token"
        )
    for user_data in users_db.values():
        if user_data["reset_token"] == user.reset_token:
            hashed_password = get_password_hash(user.new_password)
            user_data["hashed_password"] = hashed_password
            user_data["reset_token"] = None
            return {"message": "Password updated successfully"}