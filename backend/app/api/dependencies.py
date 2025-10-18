"""API dependency injection configuration."""
from typing import Generator
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.application.interfaces.image_repository import IImageRepository
from app.application.interfaces.storage_service import IStorageService
from app.infrastructure.database.repositories.image_repository import SQLAlchemyImageRepository
from app.infrastructure.external.local_storage import LocalStorageService


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database session.
    
    Yields:
        SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_image_repository(db: Session = None) -> IImageRepository:
    """
    Dependency for image repository.
    
    Note: db parameter will be injected by FastAPI via Depends(get_db)
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        Image repository implementation
    """
    if db is None:
        # Fallback for direct calls (testing)
        db = next(get_db())
    return SQLAlchemyImageRepository(db)


def get_storage_service() -> IStorageService:
    """
    Dependency for storage service.
    
    Returns:
        Storage service implementation
    """
    return LocalStorageService(upload_folder=settings.UPLOAD_FOLDER)
