from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base_model import BaseModel
from typing import Optional, List

class APIKey(BaseModel):
    """
    Represents an API Key with hashed_key, name, scopes, rate_limit, and last_used fields.
    """
    
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    hashed_key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    scopes = Column(String, nullable=True)  # JSON array as a string
    rate_limit = Column(Integer, default=100)  # Number of requests allowed per minute
    last_used = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User", back_populates="api_keys")

    def update_last_used(self):
        """
        Updates the last_used field with the current timestamp.
        """
        self.last_used = datetime.utcnow()