from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Organisation(Base):
    """
    Represents an organisation in the system.

    Attributes:
        id (int): Unique identifier for the organisation.
        name (str): Name of the organisation.
        description (str): Description of the organisation.
        users (list[User]): List of users belonging to this organisation.
    """

    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    # Relationship to associated users
    users = relationship("User", back_populates="organisation")

class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        role (str): Role of the user (e.g., 'admin', 'user').
        organisation_id (int): ID of the organisation this user belongs to.
        organisation (Organisation): The organisation this user belongs to.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), nullable=False)

    # Relationship to the associated organisation
    organisation = relationship("Organisation", back_populates="users")