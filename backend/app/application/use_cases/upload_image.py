"""Upload image use case."""
import logging
from pathlib import Path
from typing import BinaryIO

from app.domain.entities.card_image import CardImage
from app.domain.enums import ImageStatus
from app.domain.exceptions import ImageValidationError, StorageError
from app.application.interfaces.image_repository import IImageRepository
from app.application.interfaces.storage_service import IStorageService


logger = logging.getLogger(__name__)


class UploadImageUseCase:
    """
    Use case: Upload a card image.
    
    This orchestrates the business logic for uploading and storing
    a card image file. Follows Single Responsibility Principle.
    """
    
    def __init__(
        self, 
        image_repository: IImageRepository,
        storage_service: IStorageService
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            image_repository: Repository for image persistence
            storage_service: Service for file storage
        """
        self.image_repository = image_repository
        self.storage_service = storage_service
    
    async def execute(
        self, 
        file_content: BinaryIO,
        filename: str,
        content_type: str
    ) -> CardImage:
        """
        Execute the upload image use case.
        
        Args:
            file_content: Binary content of the uploaded file
            filename: Original filename
            content_type: MIME type (e.g., "image/jpeg")
            
        Returns:
            Created CardImage entity
            
        Raises:
            ImageValidationError: If image validation fails
            StorageError: If file storage fails
        """
        logger.info(f"Starting upload for file: {filename}")
        
        # 1. Validate content type
        self._validate_content_type(content_type)
        
        # 2. Save file to storage
        try:
            file_path = await self.storage_service.save_file(
                file_content, 
                filename,
                content_type
            )
            logger.info(f"File saved to: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {e}")
            raise StorageError(f"Failed to save file: {str(e)}")
        
        # 3. Create domain entity
        card_image = CardImage(
            original_path=str(file_path),
            status=ImageStatus.NON_TRAITE
        )
        
        # 4. Validate domain entity
        try:
            card_image.validate()
        except ValueError as e:
            # Cleanup: delete file if validation fails
            await self.storage_service.delete_file(str(file_path))
            logger.error(f"Image validation failed: {e}")
            raise ImageValidationError(str(e))
        
        # 5. Persist to database
        try:
            saved_image = await self.image_repository.save(card_image)
            logger.info(f"Image saved with ID: {saved_image.id}")
            return saved_image
        except Exception as e:
            # Cleanup: delete file if database save fails
            await self.storage_service.delete_file(str(file_path))
            logger.error(f"Failed to save image to database: {e}")
            raise
    
    def _validate_content_type(self, content_type: str) -> None:
        """
        Validate that content type is an accepted image format.
        
        Args:
            content_type: MIME type to validate
            
        Raises:
            ImageValidationError: If content type is not supported
        """
        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        
        if content_type not in allowed_types:
            raise ImageValidationError(
                f"Unsupported file type: {content_type}. "
                f"Allowed types: {', '.join(allowed_types)}"
            )
