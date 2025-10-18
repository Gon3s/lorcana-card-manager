"""
Unit tests for UploadImageUseCase
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from io import BytesIO

from app.application.use_cases.upload_image import UploadImageUseCase
from app.application.interfaces.image_repository import IImageRepository
from app.application.interfaces.storage_service import IStorageService
from app.domain.entities.card_image import CardImage
from app.domain.enums.image_status import ImageStatus
from app.domain.exceptions import (
    UnsupportedFileTypeError,
    FileTooLargeError,
    StorageError
)


@pytest.mark.unit
class TestUploadImageUseCase:
    """Test suite for UploadImageUseCase"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock image repository"""
        repository = Mock(spec=IImageRepository)
        repository.create = AsyncMock()
        return repository
    
    @pytest.fixture
    def mock_storage(self):
        """Create mock storage service"""
        storage = Mock(spec=IStorageService)
        storage.save_image = AsyncMock()
        return storage
    
    @pytest.fixture
    def use_case(self, mock_repository, mock_storage):
        """Create UploadImageUseCase instance"""
        return UploadImageUseCase(
            image_repository=mock_repository,
            storage_service=mock_storage
        )
    
    @pytest.fixture
    def valid_image_file(self):
        """Create a valid mock image file"""
        file = Mock()
        file.filename = "test_card.png"
        file.content_type = "image/png"
        file.file = BytesIO(b"fake image content")
        return file
    
    @pytest.mark.asyncio
    async def test_execute_success_png(self, use_case, mock_repository, mock_storage, valid_image_file):
        """Test successful image upload with PNG file"""
        # Arrange
        from pathlib import Path
        expected_path = Path("/uploads/2025-01-18/test_uuid.png")
        mock_storage.save_file.return_value = expected_path
        
        mock_image = CardImage(
            id=1,
            original_path=str(expected_path),
            status=ImageStatus.NON_TRAITE,
            created_at=datetime.now()
        )
        mock_repository.save.return_value = mock_image
        
        # Act
        result = await use_case.execute(
            valid_image_file.file,
            valid_image_file.filename,
            valid_image_file.content_type
        )
        
        # Assert
        assert result.id == 1
        assert result.original_path == str(expected_path)
        assert result.status == ImageStatus.NON_TRAITE
        mock_storage.save_file.assert_called_once_with(
            valid_image_file.file,
            "test_card.png",
            "image/png"
        )
        mock_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_success_jpg(self, use_case, mock_repository, mock_storage):
        """Test successful image upload with JPG file"""
        # Arrange
        from pathlib import Path
        jpg_file = BytesIO(b"fake jpeg content")
        filename = "card.jpg"
        content_type = "image/jpeg"
        
        expected_path = Path("/uploads/2025-01-18/test_uuid.jpg")
        mock_storage.save_file.return_value = expected_path
        
        mock_image = CardImage(
            id=2,
            original_path=str(expected_path),
            status=ImageStatus.NON_TRAITE,
            created_at=datetime.now()
        )
        mock_repository.save.return_value = mock_image
        
        # Act
        result = await use_case.execute(jpg_file, filename, content_type)
        
        # Assert
        assert result.id == 2
        assert result.original_path == str(expected_path)
        mock_storage.save_file.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_invalid_file_type(self, use_case):
        """Test upload with unsupported file type"""
        # Arrange
        from app.domain.exceptions import ImageValidationError
        file_content = BytesIO(b"fake content")
        filename = "document.pdf"
        content_type = "application/pdf"
        
        # Act & Assert
        with pytest.raises(ImageValidationError) as exc_info:
            await use_case.execute(file_content, filename, content_type)
        
        assert "Unsupported file type" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_execute_no_content_type(self, use_case):
        """Test upload with missing content type"""
        # Arrange
        from app.domain.exceptions import ImageValidationError
        file_content = BytesIO(b"content")
        filename = "test.png"
        content_type = None
        
        # Act & Assert
        with pytest.raises(ImageValidationError):
            await use_case.execute(file_content, filename, content_type)
    
    @pytest.mark.asyncio
    async def test_execute_storage_failure(self, use_case, mock_storage):
        """Test handling of storage service failure"""
        # Arrange
        mock_storage.save_file.side_effect = StorageError("Disk full")
        file_content = BytesIO(b"content")
        
        # Act & Assert
        with pytest.raises(StorageError) as exc_info:
            await use_case.execute(file_content, "test.png", "image/png")
        
        assert "Disk full" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_execute_repository_failure(self, use_case, mock_repository, mock_storage):
        """Test handling of repository failure"""
        # Arrange
        from pathlib import Path
        mock_storage.save_file.return_value = Path("/uploads/test.png")
        mock_storage.delete_file = AsyncMock(return_value=True)
        mock_repository.save.side_effect = Exception("Database error")
        file_content = BytesIO(b"content")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await use_case.execute(file_content, "test.png", "image/png")
        
        assert "Database error" in str(exc_info.value)
        # Verify cleanup was called
        mock_storage.delete_file.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_creates_correct_entity(self, use_case, mock_repository, mock_storage):
        """Test that the use case creates the correct CardImage entity"""
        # Arrange
        from pathlib import Path
        expected_path = Path("/uploads/2025-01-18/test.png")
        mock_storage.save_file.return_value = expected_path
        
        # Capture the entity passed to repository.save
        created_entity = None
        async def capture_save(entity):
            nonlocal created_entity
            created_entity = entity
            return CardImage(
                id=1,
                original_path=entity.original_path,
                status=entity.status,
                created_at=datetime.now()
            )
        
        mock_repository.save.side_effect = capture_save
        file_content = BytesIO(b"content")
        
        # Act
        await use_case.execute(file_content, "test.png", "image/png")
        
        # Assert
        assert created_entity is not None
        assert created_entity.original_path == str(expected_path)
        assert created_entity.status == ImageStatus.NON_TRAITE
        assert created_entity.processed_at is None
        assert created_entity.error_message is None
