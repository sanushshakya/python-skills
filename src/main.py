from fastapi import FastAPI, HTTPException, Depends, Security, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Initialize FastAPI app
app = FastAPI(title="User Management API", description="A simple CRUD API for managing users.")

# In-memory database simulation using a list
users_db: List[dict] = []

# User model
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None

# Dependency to fetch user by ID
def get_user(user_id: int) -> dict:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user data if found.

    Raises:
        HTTPException: If the user is not found.
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Dependency to get current active user
def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Retrieve the currently authenticated user.

    Args:
        token (str): The JWT token provided in the request headers.

    Returns:
        dict: The user data of the currently authenticated user.
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
    user = get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# CryptContext for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Endpoint to create a new user
@app.post("/auth/register", response_model=User)
def register_user(user: User):
    """
    Register a new user.

    Args:
        user (User): The user data to be created.

    Returns:
        User: The created user data.
    """
    hashed_password = pwd_context.hash(user.password)
    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password
    }
    users_db.append(new_user)
    return new_user

# Endpoint to login and receive a token
@app.post("/auth/login", response_model=User)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The username and password provided by the user.

    Returns:
        User: The authenticated user data.
    """
    user = get_user_by_email(email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"id": user["id"], "name": user["name"], "email": user["email"], "access_token": access_token, "token_type": "bearer"}

# Endpoint to forgot password and receive a reset token
@app.post("/auth/forgot-password", response_model=User)
def forgot_password(user: User):
    """
    Generate a reset token for the user.

    Args:
        user (User): The user data whose password needs to be reset.

    Returns:
        User: The user data with the reset token.
    """
    reset_token = generate_reset_token()
    user["reset_token"] = reset_token
    return user

# Endpoint to update password using a reset token
@app.post("/auth/update-password", response_model=User)
def update_password(user: User, new_password: str):
    """
    Update the user's password using a reset token.

    Args:
        user (User): The user data whose password needs to be updated.
        new_password (str): The new password for the user.

    Returns:
        User: The user data with the updated password.
    """
    if not user["reset_token"]:
        raise HTTPException(status_code=400, detail="No reset token available")
    hashed_new_password = pwd_context.hash(new_password)
    user["hashed_password"] = hashed_new_password
    user["reset_token"] = None
    return user

# Helper function to get user by email
def get_user_by_email(email: str) -> dict:
    """
    Retrieve a user by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        dict: The user data if found.
    """
    for user in users_db:
        if user["email"] == email:
            return user
    return None

# Helper function to create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The time until the token expires.

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

# Helper function to generate a reset token
def generate_reset_token():
    """
    Generate a unique reset token.

    Returns:
        str: The generated reset token.
    """
    import secrets
    return secrets.token_urlsafe(16)
```

This updated `src/main.py` file includes the necessary changes to add `hashed_password` and `reset_token` fields to the `User` model, as well as implementing the `/auth/register`, `/auth/login`, `/auth/forgot-password`, and `/auth/update-password` endpoints.