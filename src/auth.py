from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from celery import Celery

# Secret key used to encode and decode JWTs
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration times in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, ignore_result=True)
def send_password_reset_email(self, user_id: int):
    """
    Background task to send a password reset email.

    Args:
        user_id (int): The ID of the user to reset the password for.
        
    Raises:
        HTTPException: If there is an issue sending the email.
    """
    try:
        # Logic to send email
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error sending password reset email: {str(e)}")

@app.task(bind=True, ignore_result=True)
def send_email_verification_email(self, user_id: int):
    """
    Background task to send an email verification email.

    Args:
        user_id (int): The ID of the user to verify.
        
    Raises:
        HTTPException: If there is an issue sending the email.
    """
    try:
        # Logic to send email
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error sending verification email: {str(e)}")

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
    Verifies a JWT token and returns the payload.

    Args:
        token (str): The JWT token to verify.
        
    Returns:
        dict: The decoded payload of the token if valid, otherwise raises an HTTPException.
    
    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )