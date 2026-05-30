"""Module containing the Notification model."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Notification(Base):
    """
    Represents a notification in the database.
    
    Attributes:
        id (int): The primary key of the notification.
        user_id (int): The ID of the user receiving the notification.
        message (str): The content of the notification.
        created_at (datetime): The timestamp when the notification was created.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Inline comments are used to explain each field in the model