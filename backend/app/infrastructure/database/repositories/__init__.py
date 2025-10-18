"""Repository implementations - Adapters for data persistence."""
from .image_repository import SQLAlchemyImageRepository

__all__ = ["SQLAlchemyImageRepository"]
