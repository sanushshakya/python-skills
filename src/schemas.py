# src/schemas.py
from strawberry import Schema, SubscriptionType, field
from typing import List, Optional
from datetime import datetime

class User:
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        role (str): Role or permission level of the user.
    """
    id: int
    name: str
    email: str
    role: str

class Query:
    """
    Defines query operations for the GraphQL schema.

    Attributes:
        users (List[User]): List of all users in the system.
    """
    @field(name="users")
    def get_users(self, info) -> List[User]:
        # This should be replaced with actual data retrieval logic
        return [
            User(id=1, name="Alice", email="alice@example.com", role="admin"),
            User(id=2, name="Bob", email="bob@example.com", role="user")
        ]

class Mutation:
    """
    Defines mutation operations for the GraphQL schema.
    
    Attributes:
        create_user (User): Creates a new user.
    """
    @field(name="create_user")
    def create_user(self, info, name: str, email: str, role: str) -> User:
        # This should be replaced with actual data creation logic
        return User(id=3, name=name, email=email, role=role)

class Subscription(SubscriptionType):
    """
    Defines subscription operations for the GraphQL schema.

    Attributes:
        user_created (User): Subscribes to new users being created.
    """
    @field(name="user_created")
    def subscribe_user_created(self, info) -> User:
        # This should be replaced with actual data retrieval logic
        while True:
            yield User(id=3, name="New User", email="newuser@example.com", role="guest")

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)