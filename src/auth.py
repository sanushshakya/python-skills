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

# Dependency to check if the user is verified and has a valid role
def get_current_active_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to verify the JWT token and return the current active user.

    Args:
        token (str): The JWT token provided by the client.

    Returns:
        User: The current active user if verification is successful.

    Raises:
        HTTPException: If the token is invalid, expired, or not verified.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    elif not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not verified")
    return user

async def verify_role(current_user: User = Depends(get_current_active_user), required_role: str = None):
    """
    Dependency to check if the current user has a specific role.

    Args:
        current_user (User): The current active user.
        required_role (str): The required role for accessing the protected route.

    Raises:
        HTTPException: If the current user does not have the required role.
    """
    if required_role is not None and current_user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

# Example usage of the dependencies in a route
@app.post("/items/", response_model=Item)
async def create_item(item: Item, current_user: User = Depends(get_current_active_user), required_role: str = Depends(verify_role)):
    """
    Create a new item.

    Args:
        item (Item): The data for the new item.
        current_user (User): The current active user.
        required_role (str): The required role to create an item.

    Returns:
        Item: The newly created item.

    Raises:
        HTTPException: If the current user does not have the required role or is not verified.
    """
    if item.role_required and required_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return await create_item_db(item)