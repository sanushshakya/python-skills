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

# User model with role and is_verified fields
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    reset_token: Optional[str] = None
    role: str = "user"  # Default role to 'user'
    is_verified: bool = False  # New field to indicate if the user's email is verified

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

@app.post("/auth/register", response_model=User)
def register_user(form_data: RegisterRequest):
    """
    Register a new user.

    Args:
        form_data (RegisterRequest): The data for the new user.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If an email already exists.
    """
    # Check if the email is already registered
    existing_user = next((user for user in users_db if user["email"] == form_data.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    new_user_id = len(users_db) + 1
    hashed_password = pwd_context.hash(form_data.password)
    new_user = {
        "id": new_user_id,
        "name": form_data.name,
        "email": form_data.email,
        "hashed_password": hashed_password,
        "role": "user",
        "is_verified": False
    }
    users_db.append(new_user)
    return new_user

@app.post("/auth/login", response_model=User)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The username and password provided by the user.

    Returns:
        User: The authenticated user.
    """
    # Find the user in the database
    user = next((user for user in users_db if user["email"] == form_data.username), None)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Create a JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"], "is_verified": user["is_verified"], "token": access_token}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT token.

    Args:
        data (dict): The payload of the token.
        expires_delta (Optional[timedelta]): The time until the token expires. If None, the default is 30 minutes.

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

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The requested user.
    """
    user = get_user(user_id)
    return user

@app.get("/users", response_model=List[User])
def read_users():
    """
    Retrieve all users.

    Returns:
        List[User]: A list of all users.
    """
    return users_db

@app.put("/users/{user_id}", response_model=User)
@require_role("admin")
def update_user(user_id: int, user: User):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.
        user (User): The new data for the user.

    Returns:
        User: The updated user.
    """
    existing_user = get_user(user_id)
    existing_user.update(user.dict(exclude_unset=True))
    return existing_user

@app.delete("/users/{user_id}")
@require_role("admin")
def delete_user(user_id: int):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        None
    """
    global users_db
    users_db = [user for user in users_db if user["id"] != user_id]