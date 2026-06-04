from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

router = APIRouter()

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT token with the specified data and expiration time.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta, optional): The duration for which the token is valid. Defaults to None.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/auth/login", response_model=Token)
async def login_for_access_token(request: Request):
    """
    Handles the OAuth2 callback from Google and stores provider and user ID.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Token: A JSON object containing the access token.
    """
    # Placeholder logic for OAuth2 authentication with Google
    # In a real-world application, you would handle the OAuth2 flow here
    # and retrieve the provider and user ID from the callback URL

    provider = "google"
    user_id = "123456789"

    # Create a payload with the provider and user ID
    payload = {"provider": provider, "user_id": user_id}

    # Generate an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}