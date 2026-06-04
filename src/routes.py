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
    
    This route should redirect the user to the GitHub login page with a unique state parameter.
    The specific URL and parameters depend on your GitHub application configuration.
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
    if request.state != "your_expected_state_value":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid state parameter")

    # Exchange the authorization code for an access token using the GitHub API
    # (This is a placeholder for the actual logic)
    access_token = "your_access_token_here"

    # Fetch the user details from the GitHub API
    # (This is a placeholder for the actual logic)
    user_details = {
        "id": "github_user_id",
        "email": "user@example.com",
        "name": "User Name"
    }

    # Check if the email already exists in the database
    existing_user = db.query(User).filter_by(email=user_details["email"]).first()

    if existing_user:
        # If the email exists, link the accounts
        user_id = existing_user.id
    else:
        # If the email does not exist, create a new user
        user_id = User.create(db, {"email": user_details["email"], "name": user_details["name"]})

    # Create or update the user record in the database with provider and user ID
    db.query(User).filter_by(id=user_id).update({
        "provider": "github",
        "provider_user_id": user_details["id"]
    }, synchronize_session=False)
    db.commit()

    # Generate and return a JWT token for authentication
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = create_access_token(access_token_data)

    return {"access_token": access_token, "token_type": "bearer"}

# Additional routes for Google OAuth2 login can be added similarly