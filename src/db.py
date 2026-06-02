from typing import Any, Callable, Dict, Optional
from functools import wraps
from sqlalchemy.orm import Session, joinedload
from opentelemetry import trace

# Initialize OpenTelemetry tracer
tracer = trace.get_tracer(__name__)

class DataLoader:
    def __init__(self):
        self.cache = {}
        self.loaders = {}

    def register(self, key: str, loader: Callable[[Any], Any]):
        """
        Register a loader function to be used for loading data by the given key.

        Args:
            key (str): The key under which the loader is registered.
            loader (Callable[[Any], Any]): The loader function that takes a single argument and returns a result.
        """
        self.loaders[key] = loader

    def clear(self):
        """
        Clear the cache of all loaders.
        """
        self.cache.clear()

    def load(self, key: str, id: Any) -> Any:
        """
        Load data for the given key and ID.

        Args:
            key (str): The key under which the loader is registered.
            id (Any): The ID for which to load data.

        Returns:
            Any: The loaded data.
        """
        if key not in self.loaders:
            raise KeyError(f"No loader registered for key '{key}'")

        if id not in self.cache:
            with tracer.start_as_current_span("load"):
                result = self.loaders[key](id)
                self.cache[id] = result

        return self.cache[id]

def dataloader(key: str):
    """
    Decorator to create a DataLoader instance and register the decorated function as a loader.

    Args:
        key (str): The key under which the loader is registered.
    """
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        global dataloader_instance
        if not hasattr(dataloader_instance, "loaders"):
            dataloader_instance = DataLoader()
        dataloader_instance.register(key, func)
        return wrapper
    return decorator

dataloader_instance = None  # Global instance of the DataLoader

def get_dataloader() -> DataLoader:
    """
    Retrieve the global DataLoader instance.

    Returns:
        DataLoader: The global DataLoader instance.
    """
    return dataloader_instance

# Example usage in a SQLAlchemy query
@sqlalchemy.orm.sessionmaker(bind=engine)
def fetch_user_with_profile(db: Session, user_id: int) -> Dict[str, Any]:
    with tracer.start_as_current_span("fetch_user_with_profile"):
        user = db.query(User).options(joinedload(User.profile)).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "profile": {
                "id": user.profile.id,
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name,
                "bio": user.profile.bio,
                "profile_picture_url": user.profile.profile_picture_url
            }
        }

# Register the loader for fetching a user with their profile
@dataloader("user_with_profile")
def load_user_with_profile(user_id: int) -> Dict[str, Any]:
    return fetch_user_with_profile(get_db(), user_id)

# Usage example in a GraphQL resolver
async def resolve_user(root, info, user_id):
    """
    Resolver function for fetching a user with their profile.

    Args:
        root (Any): The parent object from which the field is accessed.
        info (GraphQlResolveInfo): Information about the current query execution state.
        user_id (int): The ID of the user to fetch.

    Returns:
        Dict[str, Any]: A dictionary containing user and profile information.
    """
    return await dataloader_instance.load("user_with_profile", user_id)