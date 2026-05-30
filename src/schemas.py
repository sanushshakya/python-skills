from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """ Base model for user data """
    name: str
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    """ Schema for creating a new user """
    password: str

class UserUpdate(UserBase):
    """ Schema for updating an existing user """
    password: str | None = None

class User(UserBase):
    """ Schema for returning a user """
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserProfile(BaseModel):
    """ Schema for user profile information """
    bio: str | None = None
    location: str | None = None
    interests: list[str] | None = None

class UserWithProfile(User):
    """ Schema for returning a user with their profile information """
    profile: UserProfile