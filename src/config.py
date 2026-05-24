"""
Configuration module for the User Management API.

This module contains all the configuration constants used across the application.
"""

# Define the API version
API_VERSION: str = "1.0.0"

# Define the database settings
DATABASE_HOST: str = "localhost"
DATABASE_PORT: int = 5432
DATABASE_USER: str = "user_management"
DATABASE_PASSWORD: str = "securepassword"
DATABASE_NAME: str = "user_db"

# Define the application settings
APP_DEBUG_MODE: bool = True
APP_RELOAD_MODE: bool = True

# Define the pagination settings
DEFAULT_PAGE_SIZE: int = 10
MAX_PAGE_SIZE: int = 50

# Function to get database URL
def get_database_url() -> str:
    """
    Construct the database URL using configuration constants.

    Returns:
        str: The constructed database URL.
    """
    return f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Function to validate pagination parameters
def validate_pagination(page: int, page_size: int) -> None:
    """
    Validate the pagination parameters.

    Args:
        page (int): The requested page number.
        page_size (int): The requested page size.

    Raises:
        HTTPException: If the pagination parameters are invalid.
    """
    if page < 1:
        raise ValueError("Page must be greater than or equal to 1.")
    if not (DEFAULT_PAGE_SIZE <= page_size <= MAX_PAGE_SIZE):
        raise ValueError(f"Page size must be between {DEFAULT_PAGE_SIZE} and {MAX_PAGE_SIZE}.")