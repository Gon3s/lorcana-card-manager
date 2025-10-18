"""Storage service interface (Port)."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class IStorageService(ABC):
    """
    Storage service interface for file operations.
    
    This is a Port in Clean Architecture - abstracts file storage
    implementation (local, S3, etc.).
    """
    
    @abstractmethod
    async def save_file(
        self, 
        file_content: BinaryIO, 
        filename: str,
        content_type: str
    ) -> Path:
        """
        Save uploaded file to storage.
        
        Args:
            file_content: Binary file content
            filename: Original filename
            content_type: MIME type (e.g., "image/jpeg")
            
        Returns:
            Path where file was saved
            
        Raises:
            StorageError: If save operation fails
        """
        pass
    
    @abstractmethod
    async def get_file_path(self, filename: str) -> Path:
        """
        Get full path to stored file.
        
        Args:
            filename: Filename to locate
            
        Returns:
            Full path to file
        """
        pass
    
    @abstractmethod
    async def delete_file(self, filepath: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            filepath: Path to file
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    async def file_exists(self, filepath: str) -> bool:
        """
        Check if file exists in storage.
        
        Args:
            filepath: Path to check
            
        Returns:
            True if exists, False otherwise
        """
        pass
