from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User, UserProfile
from src.schemas import UserProfileUpdateSchema, UserProfilePictureUploadSchema
from src.auth import JWTBearer, get_current_user
from src.utils import save_file_to_disk

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

@router.put("/users/me/picture", response_model=UserProfile)
async def update_user_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the current user's profile picture.

    Args:
        file (UploadFile): The uploaded image file.
        current_user (User): The authenticated user making the request.
        db (Session): Database session dependency.

    Returns:
        UserProfile: The updated user profile with the new picture URL.
    """
    # Save the file to disk and get the file path
    file_path = save_file_to_disk(file)
    
    # Update the user's profile picture URL
    current_user.profile.picture_url = file_path

    # Commit the changes to the database
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user.profile