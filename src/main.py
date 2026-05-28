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

# User model with role field
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    role: str = "user"  # Default role to 'user'

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

# Dependency to require a specific role for routes
def require_role(required_role: str):
    """
    Dependency to check if the current user has the required role.

    Args:
        required_role (str): The role required for accessing the route.

    Returns:
        dict: The user data of the currently authenticated user if they have the required role.
    """
    def inner_dependency(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return inner_dependency

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
        "hashed_password": hashed_password,
        "role": user.role
    }
    users_db.append(new_user)
    return new_user

# Endpoint to login and receive a token
@app.post("/auth/login", response_model=User)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to receive a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The user credentials for logging in.

    Returns:
        User: The user data of the currently authenticated user.
    """
    user = get_user_by_email(email=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    user["token"] = access_token
    return user

# Helper function to create a JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (Optional[timedelta]): The time until the token expires.

    Returns:
        str: The JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint to get all users (admin only)
@app.get("/users", response_model=List[User])
def get_users(current_user: dict = Depends(require_role("admin"))):
    """
    Get all users.

    Args:
        current_user (dict): The currently authenticated user, required to have the 'admin' role.

    Returns:
        List[User]: A list of all users.
    """
    return users_db

# Endpoint to get a single user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int, current_user: dict = Depends(require_role("admin"))):
    """
    Get a single user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        current_user (dict): The currently authenticated user, required to have the 'admin' role.

    Returns:
        User: The requested user data.
    """
    return get_user(user_id)

# Endpoint to update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User, current_user: dict = Depends(require_role("admin"))):
    """
    Update a user.

    Args:
        user_id (int): The ID of the user to update.
        updated_user (User): The new data for the user.
        current_user (dict): The currently authenticated user, required to have the 'admin' role.

    Returns:
        User: The updated user data.
    """
    user = get_user(user_id)
    user["name"] = updated_user.name
    user["email"] = updated_user.email
    user["hashed_password"] = pwd_context.hash(updated_user.password)
    user["role"] = updated_user.role
    return user

# Endpoint to delete a user (admin only)
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: dict = Depends(require_role("admin"))):
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.
        current_user (dict): The currently authenticated user, required to have the 'admin' role.

    Returns:
        None
    """
    global users_db
    users_db = [user for user in users_db if user["id"] != user_id]