from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User, UserProfile
from src.schemas import UserProfileUpdateSchema
from src.auth import JWTBearer, get_current_user

router = APIRouter()

@router.put("/users/me", response_model=UserProfile)
async def update_user_profile(
    user_profile: UserProfileUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the current user's profile.

    Args:
        user_profile (UserProfileUpdateSchema): Updated user profile data.
        current_user (User): The authenticated user making the request.
        db (Session): Database session dependency.

    Returns:
        UserProfile: The updated user profile.
    """
    # Fetch the user from the database
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update user profile attributes
    for field in user_profile.dict(exclude_unset=True):
        setattr(user.profile, field, getattr(user_profile, field))

    # Commit the changes to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.profile