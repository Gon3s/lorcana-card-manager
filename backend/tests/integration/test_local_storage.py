"""
Integration tests for LocalStorageService
"""
import pytest
import os
from io import BytesIO
from pathlib import Path

from app.infrastructure.external.local_storage import LocalStorageService
from app.domain.exceptions import StorageError


@pytest.mark.integration
class TestLocalStorageService:
    """Test suite for LocalStorageService"""
    
    @pytest.fixture
    def storage_service(self, temp_upload_dir):
        """Create storage service with temporary directory"""
        return LocalStorageService(upload_folder=temp_upload_dir)
    
    @pytest.mark.asyncio
    async def test_save_image_png(self, storage_service, temp_upload_dir):
        """Test saving a PNG image file"""
        # Arrange
        file_content = b"fake PNG image content"
        file = BytesIO(file_content)
        filename = "test_card.png"
        content_type = "image/png"
        
        # Act
        saved_path = await storage_service.save_file(file, filename, content_type)
        
        # Assert
        assert saved_path is not None
        assert str(saved_path).endswith(".png")
        assert os.path.exists(saved_path)
        
        # Verify content
        with open(saved_path, "rb") as f:
            assert f.read() == file_content
    
    @pytest.mark.asyncio
    async def test_save_image_jpg(self, storage_service):
        """Test saving a JPG image file"""
        # Arrange
        file_content = b"fake JPEG image content"
        file = BytesIO(file_content)
        filename = "card.jpg"
        content_type = "image/jpeg"
        
        # Act
        saved_path = await storage_service.save_file(file, filename, content_type)
        
        # Assert
        assert str(saved_path).endswith(".jpg")
        assert os.path.exists(saved_path)
    
    @pytest.mark.asyncio
    async def test_save_creates_directory_structure(self, storage_service, temp_upload_dir):
        """Test that save_file creates date-based directory structure"""
        # Arrange
        file = BytesIO(b"content")
        filename = "test.png"
        content_type = "image/png"
        
        # Act
        saved_path = await storage_service.save_file(file, filename, content_type)
        
        # Assert
        path_parts = Path(saved_path).parts
        # Should contain year-month-day directory (e.g., 2025-01-18)
        assert any("-" in part for part in path_parts)
    
    @pytest.mark.asyncio
    async def test_save_generates_unique_names(self, storage_service):
        """Test that multiple saves generate unique filenames"""
        # Arrange
        file1 = BytesIO(b"content1")
        file2 = BytesIO(b"content2")
        filename = "same_name.png"
        content_type = "image/png"
        
        # Act
        path1 = await storage_service.save_file(file1, filename, content_type)
        path2 = await storage_service.save_file(file2, filename, content_type)
        
        # Assert
        assert path1 != path2
        assert os.path.exists(path1)
        assert os.path.exists(path2)
    
    @pytest.mark.asyncio
    async def test_save_preserves_extension(self, storage_service):
        """Test that file extension is preserved"""
        # Arrange
        extensions = [".png", ".jpg", ".jpeg"]
        
        for ext in extensions:
            file = BytesIO(b"content")
            filename = f"test{ext}"
            content_type = "image/png" if ext == ".png" else "image/jpeg"
            
            # Act
            saved_path = await storage_service.save_file(file, filename, content_type)
            
            # Assert
            assert str(saved_path).endswith(ext)
    
    @pytest.mark.asyncio
    async def test_save_handles_long_filename(self, storage_service):
        """Test handling of very long filenames"""
        # Arrange
        file = BytesIO(b"content")
        long_filename = "a" * 300 + ".png"  # Very long filename
        content_type = "image/png"
        
        # Act
        saved_path = await storage_service.save_file(file, long_filename, content_type)
        
        # Assert
        assert os.path.exists(saved_path)
        assert str(saved_path).endswith(".png")
    
    @pytest.mark.asyncio
    async def test_save_handles_special_characters(self, storage_service):
        """Test handling of special characters in filename"""
        # Arrange
        file = BytesIO(b"content")
        filename = "card_épée_é.png"
        content_type = "image/png"
        
        # Act
        saved_path = await storage_service.save_file(file, filename, content_type)
        
        # Assert
        assert os.path.exists(saved_path)
