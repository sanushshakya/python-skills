from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def generate_email_verification_token(user_id: int):
    """
    Generates a JWT token for email verification.
    
    Args:
        user_id (int): The ID of the user to verify.
        
    Returns:
        str: A JWT token for email verification.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_access_token(sub: str):
    """
    Generates a JWT access token.
    
    Args:
        sub (str): The subject of the token (usually user ID).
        
    Returns:
        str: A JWT access token.
    """
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_refresh_token(sub: str):
    """
    Generates a JWT refresh token.
    
    Args:
        sub (str): The subject of the token (usually user ID).
        
    Returns:
        str: A JWT refresh token.
    """
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifies a JWT token and returns the subject.
    
    Args:
        token (str): The JWT token to verify.
        
    Returns:
        str: The subject of the verified token.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

def verify_email_verification_token(token: str):
    """
    Verifies an email verification token and returns the user ID.
    
    Args:
        token (str): The email verification token to verify.
        
    Returns:
        int: The user ID associated with the verified token.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

def trigger_login_notification(user_id: int):
    """
    Triggers a login notification for the given user ID.
    
    Args:
        user_id (int): The ID of the user logging in.
        
    Returns:
        None
    """
    # Logic to trigger a notification
    print(f"Notification triggered for user {user_id} logging in from a new device.")

def trigger_password_change_notification(user_id: int):
    """
    Triggers a password change notification for the given user ID.
    
    Args:
        user_id (int): The ID of the user changing their password.
        
    Returns:
        None
    """
    # Logic to trigger a notification
    print(f"Notification triggered for user {user_id} changing their password.")

# Update the login route to include notification triggering
def login(user: User, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns JWT tokens.
    
    Args:
        user (User): The user credentials provided during login.
        db (Session): Database session dependency.
        
    Returns:
        dict: A dictionary containing access token, refresh token, and token type.
    
    Raises:
        HTTPException: If the user does not exist or the password is incorrect.
    """
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    # Trigger login notification
    trigger_login_notification(user_db.id)
    
    access_token = generate_access_token(str(user_db.id))
    refresh_token = generate_refresh_token(str(user_db.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Update the change_password route to include notification triggering
def change_password(user_id: int, new_password: str, current_password: str, db: Session = Depends(get_db)):
    """
    Changes a user's password.
    
    Args:
        user_id (int): The ID of the user changing their password.
        new_password (str): The new password for the user.
        current_password (str): The current password of the user.
        db (Session): Database session dependency.
        
    Returns:
        dict: A dictionary indicating success or failure.
    
    Raises:
        HTTPException: If the user does not exist, the current password is incorrect, or the new password is too short.
    """
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db or not verify_password(current_password, user_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect current password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    # Check password length
    if len(new_password) < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Password must be at least 8 characters long")
    
    user_db.password = get_password_hash(new_password)
    db.commit()
    
    # Trigger password change notification
    trigger_password_change_notification(user_id)
    
    return {"detail": "Password changed successfully"}