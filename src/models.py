from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GitHubOAuth2Provider(Base):
    """
    Model to store details of the GitHub OAuth2 provider.
    
    This model will be used to store the client ID and client secret for the GitHub OAuth2 authentication.
    """

    __tablename__ = 'github_oauth2_provider'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    client_secret = Column(String, nullable=False)

    # Relationships
    users = relationship('User', back_populates='github_oauth2_provider')

class User(Base):
    """
    Model to represent a user in the system.
    
    This model includes details about the user such as name, email, role, and links to OAuth2 provider details.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationship to GitHub OAuth2 provider
    github_oauth2_provider_id = Column(Integer, ForeignKey('github_oauth2_provider.id'), index=True)
    github_oauth2_provider = relationship("GitHubOAuth2Provider", back_populates="users")

# Example usage in other parts of the application
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
# Base.metadata.create_all(bind=engine)