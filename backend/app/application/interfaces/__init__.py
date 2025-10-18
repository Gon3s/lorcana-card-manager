"""Application interfaces (Ports) - Abstract contracts."""
from .image_repository import IImageRepository
from .storage_service import IStorageService

__all__ = ["IImageRepository", "IStorageService"]
