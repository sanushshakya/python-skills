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
    Login a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The user's email and password.

    Returns:
        User: The authenticated user data.
    """
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# Endpoint to update an existing user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User, current_user: dict = Depends(get_current_user)):
    """
    Update an existing user.

    Args:
        user_id (int): The ID of the user to update.
        updated_user (User): The new data for the user.
        current_user (dict): The currently authenticated user.

    Returns:
        User: The updated user data.
    """
    if not current_user["id"] == user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
    user = get_user(user_id)
    user.update({"name": updated_user.name, "email": updated_user.email})
    return user

# Endpoint to delete a user
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """
    Delete an existing user.

    Args:
        user_id (int): The ID of the user to delete.
        current_user (dict): The currently authenticated user.

    Returns:
        None
    """
    if not current_user["id"] == user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    global users_db
    users_db = [user for user in users_db if user["id"] != user_id]

# Endpoint to list all users
@app.get("/users", response_model=List[User])
def list_users(current_user: dict = Depends(get_current_user)):
    """
    List all users.

    Args:
        current_user (dict): The currently authenticated user.

    Returns:
        List[User]: A list of all users.
    """
    return users_db

# Helper function to authenticate a user
def authenticate_user(users: List[dict], username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user by checking the email and password.

    Args:
        users (List[dict]): The list of users.
        username (str): The user's email.
        password (str): The user's password.

    Returns:
        dict: The authenticated user if found, None otherwise.
    """
    for user in users:
        if user["email"] == username and pwd_context.verify(password, user["hashed_password"]):
            return user
    return None

# Helper function to create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (Optional[timedelta]): The expiration time for the token.

    Returns:
        str: The JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt