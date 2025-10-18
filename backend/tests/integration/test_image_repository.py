"""
Integration tests for SQLAlchemyImageRepository
"""
import pytest
from datetime import datetime

from app.infrastructure.database.repositories.image_repository import SQLAlchemyImageRepository
from app.domain.entities.card_image import CardImage
from app.domain.enums.image_status import ImageStatus


@pytest.mark.integration
class TestSQLAlchemyImageRepository:
    """Test suite for SQLAlchemyImageRepository"""
    
    @pytest.fixture
    def repository(self, test_db):
        """Create repository instance with test database"""
        return SQLAlchemyImageRepository(test_db)
    
    @pytest.mark.asyncio
    async def test_create_image(self, repository):
        """Test creating a new image record"""
        # Arrange
        image_entity = CardImage(
            original_path="/uploads/2025-01-18/test.png",
            status=ImageStatus.NON_TRAITE
        )
        
        # Act
        result = await repository.save(image_entity)
        
        # Assert
        assert result.id is not None
        assert result.id > 0
        assert result.original_path == "/uploads/2025-01-18/test.png"
        assert result.status == ImageStatus.NON_TRAITE
        assert result.created_at is not None
        assert isinstance(result.created_at, datetime)
    
    @pytest.mark.asyncio
    async def test_get_by_id_existing(self, repository):
        """Test retrieving an existing image by ID"""
        # Arrange
        created = await repository.save(CardImage(
            original_path="/uploads/test1.png",
            status=ImageStatus.NON_TRAITE
        ))
        
        # Act
        result = await repository.get_by_id(created.id)
        
        # Assert
        assert result is not None
        assert result.id == created.id
        assert result.original_path == created.original_path
        assert result.status == created.status
    
    @pytest.mark.asyncio
    async def test_get_by_id_non_existing(self, repository):
        """Test retrieving a non-existing image returns None"""
        # Act
        result = await repository.get_by_id(999999)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_image(self, repository):
        """Test updating an existing image"""
        # Arrange
        created = await repository.save(CardImage(
            original_path="/uploads/test.png",
            status=ImageStatus.NON_TRAITE
        ))
        
        # Modify entity
        created.status = ImageStatus.EN_COURS
        created.processed_at = datetime.now()
        
        # Act
        result = await repository.update(created)
        
        # Assert
        assert result.id == created.id
        assert result.status == ImageStatus.EN_COURS
        assert result.processed_at is not None
        
        # Verify persistence
        retrieved = await repository.get_by_id(created.id)
        assert retrieved.status == ImageStatus.EN_COURS
    
    @pytest.mark.asyncio
    async def test_update_with_error(self, repository):
        """Test updating image with error message"""
        # Arrange
        created = await repository.save(CardImage(
            original_path="/uploads/test.png",
            status=ImageStatus.NON_TRAITE
        ))
        
        # Modify with error
        created.status = ImageStatus.ERROR
        created.error_message = "OCR processing failed"
        created.processed_at = datetime.now()
        
        # Act
        result = await repository.update(created)
        
        # Assert
        assert result.status == ImageStatus.ERROR
        assert result.error_message == "OCR processing failed"
        assert result.processed_at is not None
    
    @pytest.mark.asyncio
    async def test_multiple_images(self, repository):
        """Test creating and retrieving multiple images"""
        # Arrange & Act
        image1 = await repository.save(CardImage(
            original_path="/uploads/card1.png",
            status=ImageStatus.NON_TRAITE
        ))
        
        image2 = await repository.save(CardImage(
            original_path="/uploads/card2.jpg",
            status=ImageStatus.EN_COURS
        ))
        
        # Assert
        assert image1.id != image2.id
        
        retrieved1 = await repository.get_by_id(image1.id)
        retrieved2 = await repository.get_by_id(image2.id)
        
        assert retrieved1.original_path == "/uploads/card1.png"
        assert retrieved2.original_path == "/uploads/card2.jpg"
        assert retrieved1.status == ImageStatus.NON_TRAITE
        assert retrieved2.status == ImageStatus.EN_COURS
