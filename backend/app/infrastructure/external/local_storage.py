"""Local file storage service implementation."""
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import BinaryIO
import aiofiles

from app.application.interfaces.storage_service import IStorageService
from app.domain.exceptions import StorageError


logger = logging.getLogger(__name__)


class LocalStorageService(IStorageService):
    """
    Local file system storage implementation (Adapter).
    
    Implements IStorageService interface for local file storage.
    Could be swapped with S3StorageService without changing business logic.
    """
    
    def __init__(self, upload_folder: str):
        """
        Initialize storage service with upload folder.
        
        Args:
            upload_folder: Base directory for uploads
        """
        self.upload_folder = Path(upload_folder)
        self._ensure_upload_folder_exists()
    
    def _ensure_upload_folder_exists(self) -> None:
        """Create upload folder if it doesn't exist."""
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Upload folder ensured: {self.upload_folder}")
    
    async def save_file(
        self, 
        file_content: BinaryIO, 
        filename: str,
        content_type: str
    ) -> Path:
        """
        Save uploaded file to local storage.
        
        Args:
            file_content: Binary file content
            filename: Original filename
            content_type: MIME type
            
        Returns:
            Path where file was saved
            
        Raises:
            StorageError: If save operation fails
        """
        try:
            # Create date-based subfolder (YYYY-MM-DD)
            date_folder = datetime.now().strftime("%Y-%m-%d")
            target_folder = self.upload_folder / date_folder
            target_folder.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            extension = Path(filename).suffix
            unique_filename = f"{uuid.uuid4()}{extension}"
            file_path = target_folder / unique_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = file_content.read()
                await f.write(content)
            
            logger.info(f"File saved successfully: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {e}")
            raise StorageError(f"Failed to save file: {str(e)}")
    
    async def get_file_path(self, filename: str) -> Path:
        """
        Get full path to stored file.
        
        Args:
            filename: Filename to locate
            
        Returns:
            Full path to file
        """
        # If filename is already a full path, return it
        file_path = Path(filename)
        if file_path.is_absolute():
            return file_path
        
        # Otherwise, search in upload folder
        return self.upload_folder / filename
    
    async def delete_file(self, filepath: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            filepath: Path to file
            
        Returns:
            True if deleted, False if not found
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                logger.warning(f"File not found for deletion: {filepath}")
                return False
            
            file_path.unlink()
            logger.info(f"File deleted: {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to delete file {filepath}: {e}")
            raise StorageError(f"Failed to delete file: {str(e)}")
    
    async def file_exists(self, filepath: str) -> bool:
        """
        Check if file exists in storage.
        
        Args:
            filepath: Path to check
            
        Returns:
            True if exists, False otherwise
        """
        return Path(filepath).exists()
