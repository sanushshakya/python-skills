# src/celery.py
"""
Celery configuration for the User Management API.

This module sets up a Celery application to handle background tasks asynchronously using Redis as the message broker.
"""

from celery import Celery

def create_celery_app():
    """
    Creates and configures a Celery app instance with Redis as the broker.

    Returns:
        Celery: A configured Celery app instance.
    """
    # Create a new Celery app instance
    celery_app = Celery(
        __name__,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )

    # Configure the Celery app with default settings
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],  # Ignore other content types
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )

    return celery_app

celery = create_celery_app()