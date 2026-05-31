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
```

This file defines the `Organisation` model for SQLAlchemy ORM. The `__tablename__` attribute specifies the table name in the database. The `id`, `name`, and `description` fields are defined as columns with appropriate types. The `users` field establishes a one-to-many relationship with the `User` model, allowing us to access all users associated with an organisation through this model.