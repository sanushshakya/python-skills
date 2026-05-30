from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    """
    Pydantic model for JWT token response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Pydantic model for data extracted from JWT token.
    """
    username: str = None
    scopes: list = []

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT access token.

    Returns:
        dict: The data of the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return {"username": token_data.username}

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Endpoint to retrieve the current user's profile.

    Args:
        current_user (dict): The data of the current user, provided by the dependency.

    Returns:
        dict: The data of the current user.
    """
    return current_user