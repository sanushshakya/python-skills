from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GoogleOAuth2Provider(Base):
    """
    SQLAlchemy model for storing Google OAuth2 provider details.
    This model is used to store the client ID and client secret required for authenticating with Google's OAuth2 service.
    """

    __tablename__ = "google_oauth2_providers"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    client_secret = Column(String, nullable=False)

    def __repr__(self):
        return f"<GoogleOAuth2Provider(id={self.id}, client_id={self.client_id})>"