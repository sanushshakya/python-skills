"""
Authentication module for the User Management API.

This module contains functions to manage user authentication using JWT.
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
        user_id (int): The ID of the user to verify.

    Returns:
        str: A JWT that can be used to verify the user's email.
    """
    # Set the expiration time for the token
    expire = datetime.utcnow() + timedelta(days=1)
    
    # Create a payload with the necessary information
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    
    # Encode the payload into a JWT
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# Example usage:
# token = generate_email_verification_token(123)