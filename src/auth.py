"""
Authentication module for the User Management API.

This module contains functions to manage user authentication using JWT, including email verification and token refresh functionality.
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

def generate_access_token(data: dict, expires_delta: timedelta):
    """
    Generates a JWT for access.

    Args:
        data (dict): Data to be encoded in the token.
        expires_delta (timedelta): Expiration time for the token.

    Returns:
        str: A JWT containing the provided data and expiration time.
    """
    payload = copy.deepcopy(data)
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def generate_refresh_token(user_id: int):
    """
    Generates a JWT for refresh.

    Args:
        user_id (int): The ID of the user to whom the token is issued.

    Returns:
        str: A JWT containing the user's ID and expiration time.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
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

async def verify_access_token(token: str):
    """
    Verifies a JWT for access.

    Args:
        token (str): The JWT to be verified.

    Returns:
        dict: The payload of the token if verification is successful.

    Raises:
        HTTPException: If the token is invalid, expired, or not verified.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

async def verify_refresh_token(token: str):
    """
    Verifies a JWT for refresh.

    Args:
        token (str): The JWT to be verified.

    Returns:
        int: The user ID contained in the token if verification is successful.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
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
        required_role (str): The required role for the operation. If None, no role check is performed.

    Returns:
        bool: True if the user has the required role, False otherwise.
    """
    if required_role is not None and current_user.role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return True

# Update /auth/login Endpoint — Return both access and refresh tokens
@app.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login for access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing the username and password.

    Returns:
        Token: A dictionary containing both access and refresh tokens.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = generate_refresh_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.post("/auth/refresh_token", response_model=Token)
async def refresh_access_token(token: str = Depends(oauth2_scheme)):
    """
    Refresh access token.

    Args:
        token (str): The refresh token provided by the client.

    Returns:
        Token: A dictionary containing a new access token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = generate_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": new_access_token, "token_type": "bearer"}