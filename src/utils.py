"""
Utility functions for the User Management API.

This module contains shared helper functions that can be reused across different parts of the application.
"""

from fastapi import HTTPException
from typing import Any, Dict, List

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