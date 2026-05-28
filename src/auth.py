"""
Authentication module for the User Management API.

This module contains functions to manage user authentication using JWT, including email verification.
"""

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

def generate_email_verification_token(user_id: int):
    """
    Generates a JWT for email verification.

    Args:
        user_id (int): The ID of the user to whom the token is issued.

    Returns:
        str: A JWT containing the user's ID and expiration time.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verify_email_verification_token(token: str):
    """
    Verifies a JWT for email verification.

    Args:
        token (str): The JWT to be verified.

    Returns:
        int: The user ID contained in the token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# Endpoint to resend verification emails (to be implemented in src/main.py)