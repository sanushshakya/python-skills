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

def find_user_by_id(users: List[Dict[str, Any]], user_id: int) -> Dict[str, Any]:
    """
    Find a user by their ID from a list of users.

    Args:
        users (List[Dict[str, Any]]): The list of users to search.
        user_id (int): The ID of the user to find.

    Returns:
        Dict[str, Any]: The user if found, otherwise None.
    """
    return next((user for user in users if user['id'] == user_id), None)

def generate_user_id(users: List[Dict[str, Any]]) -> int:
    """
    Generate a unique user ID based on the existing list of users.

    Args:
        users (List[Dict[str, Any]]): The list of existing users.

    Returns:
        int: A new unique user ID.
    """
    return max((user['id'] for user in users), default=0) + 1

def remove_user_by_id(users: List[Dict[str, Any]], user_id: int) -> None:
    """
    Remove a user by their ID from the list of users.

    Args:
        users (List[Dict[str, Any]]): The list of users to modify.
        user_id (int): The ID of the user to remove.
    """
    global users_db
    users_db = [user for user in users if user['id'] != user_id]