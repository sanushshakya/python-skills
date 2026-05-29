"""
Utility functions for handling JWT encoding and decoding.

This module contains shared helper functions to encode, decode, refresh JWT tokens,
and validate user data that can be reused across different parts of the application.
"""

from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any, Dict

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def generate_jwt_token(data: Dict[str, Any], expires_delta: timedelta = None):
    """
    Generates a JWT token.

    Args:
        data (Dict[str, Any]): Data to encode in the token.
        expires_delta (timedelta): Optional time delta until expiration. If not provided,
                                  uses ACCESS_TOKEN_EXPIRE_MINUTES as default.

    Returns:
        str: The encoded JWT token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Dict[str, Any]: The decoded payload of the JWT token.
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

def refresh_jwt_token(refresh_token: str):
    """
    Refreshes a JWT token.

    Args:
        refresh_token (str): The current JWT refresh token.

    Returns:
        Dict[str, Any]: A dictionary containing new access and refresh tokens.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = generate_jwt_token(data={"user_id": user_id})
    return {"access_token": new_access_token, "refresh_token": refresh_token}

def validate_user_data(user: Dict[str, Any]) -> None:
    """
    Validate user data before creating or updating a user.

    Args:
        user (Dict[str, Any]): The user data to validate.

    Raises:
        HTTPException: If the user data is invalid.
    """
    if not isinstance(user.get('name'), str) or not user['name'].strip():
        raise HTTPException(status_code=400, detail="Invalid name provided")
    
    if not isinstance(user.get('email'), str) or not user['email'].strip() or "@" not in user['email']:
        raise HTTPException(status_code=400, detail="Invalid email provided")

    if 'role' in user and not isinstance(user['role'], str):
        raise HTTPException(status_code=400, detail="Invalid role provided")