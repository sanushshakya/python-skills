"""Routes for handling OAuth2 login and account linking."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.auth import create_access_token, verify_token
from src.models import User
from src.database import get_db

router = APIRouter()

class OAuthCallbackRequest(BaseModel):
    """Pydantic model for the GitHub OAuth2 callback request."""
    state: str
    code: str

@router.get("/github/login")
async def github_login():
    """
    Redirect the user to the GitHub login page.
    """
    # Implement the logic to redirect the user to the GitHub login page with a unique state parameter
    pass

@router.get("/github/callback", response_model=User)
async def github_callback(request: OAuthCallbackRequest, db: Session = Depends(get_db)):
    """
    Handle the GitHub OAuth2 callback and store provider and user ID.
    
    Args:
        request (OAuthCallbackRequest): The GitHub OAuth2 callback request containing state and code parameters.
        db (Session, optional): SQLAlchemy session dependency. Defaults to Depends(get_db).
        
    Returns:
        User: The created or updated user record.
    """
    # Implement the logic to handle the GitHub OAuth2 callback
    # Verify the state parameter for CSRF protection
    # Exchange the authorization code for an access token using the GitHub API
    # Fetch the user details from the GitHub API
    # Create or update the user record in the database with provider and user ID
    
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")

# Additional routes for Google OAuth2 login can be added similarly
```

Please note that this is a skeleton implementation and does not include actual logic for interacting with GitHub's OAuth2 API or handling the state parameter for CSRF protection. You will need to implement these details based on your specific requirements and security considerations.