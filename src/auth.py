"""
Authentication module for the User Management API.

This module contains functions to manage user authentication using JWT.
"""

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Pydantic model for the registration request
class RegisterRequest(BaseModel):
    """
    Model for user registration request.
    
    Fields:
    - name: str
    - email: str
    - password: str
    - role: str (optional, default is 'user')
    """
    name: str
    email: str
    password: str
    role: str = "user"

# Dependency to decode JWT token and extract user data
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to decode JWT token and return user data.
    
    Raises:
    - HTTPException 401 Unauthorized if the token is invalid or expired
    
    Returns:
    - User: The decoded user data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=email)
    if user is None:
        raise credentials_exception
    return user

# Dependency to check if the current user has a specific role
def require_role(role: str):
    """
    Dependency function to check if the current user has a specific role.
    
    Args:
    - role (str): The required role
    
    Returns:
    - User: The current user data if they have the required role, otherwise raises an HTTPException
    
    Raises:
    - HTTPException 403 Forbidden if the current user does not have the required role
    """
    def inner(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return inner
```

Note: The `get_user` function is assumed to be defined elsewhere in your project. It should take an email as input and return a User object if the user exists, otherwise it should return None.