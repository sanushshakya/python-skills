# src/schemas.py
from strawberry import Schema
from strawberry.field import field
from strawberry.type import StrawberryType
from typing import List, Optional

class User(StrawberryType):
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

schema = Schema(query=Query, mutation=Mutation)