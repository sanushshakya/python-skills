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
        str: A JWT containing the user ID.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verify_email_token(token: str):
    """
    Verifies a JWT for email verification.

    Args:
        token (str): The JWT to verify.

    Returns:
        int: The user ID contained in the JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")

# Example usage in an endpoint
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/auth/verify-email/")
async def verify_email_endpoint(token: str):
    """
    Endpoint to verify user emails using a token.

    Args:
        token (str): The JWT for email verification.

    Returns:
        dict: A message indicating the verification status.
    """
    user_id = await verify_email_token(token)
    # Logic to mark the user's email as verified in your database
    return {"message": f"Email verified successfully for user ID {user_id}"}