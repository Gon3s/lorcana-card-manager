"""SQLAlchemy implementation of IImageRepository."""
import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from app.application.interfaces.image_repository import IImageRepository
from app.domain.entities.card_image import CardImage
from app.domain.enums import ImageStatus
# Use existing ORM model for now (to avoid table redefinition)
from app.models.card_image import CardImage as CardImageModel


logger = logging.getLogger(__name__)


class SQLAlchemyImageRepository(IImageRepository):
    """
    SQLAlchemy implementation of image repository (Adapter).
    
    This is an infrastructure concern - implements the repository
    interface using SQLAlchemy ORM.
    """
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
    
    async def save(self, image: CardImage) -> CardImage:
        """
        Persist a card image to database.
        
        Args:
            image: CardImage domain entity
            
        Returns:
            CardImage with assigned ID
        """
        # Convert domain entity to ORM model
        db_image = CardImageModel(
            original_path=image.original_path,
            status=image.status.value,
            card_id=image.card_id,
            processed_at=image.processed_at,
            error_message=image.error_message
        )
        
        self.session.add(db_image)
        self.session.commit()
        self.session.refresh(db_image)
        
        logger.info(f"Saved image with ID: {db_image.id}")
        
        # Convert ORM model back to domain entity
        return self._to_entity(db_image)
    
    async def get_by_id(self, image_id: int) -> Optional[CardImage]:
        """
        Retrieve card image by ID.
        
        Args:
            image_id: Image ID
            
        Returns:
            CardImage entity or None if not found
        """
        db_image = self.session.query(CardImageModel).filter(
            CardImageModel.id == image_id
        ).first()
        
        if not db_image:
            return None
        
        return self._to_entity(db_image)
    
    async def list_by_status(
        self, 
        status: ImageStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[CardImage]:
        """
        List card images by status with pagination.
        
        Args:
            status: Filter by status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of CardImage entities
        """
        db_images = self.session.query(CardImageModel).filter(
            CardImageModel.status == status.value
        ).offset(skip).limit(limit).all()
        
        return [self._to_entity(img) for img in db_images]
    
    async def update(self, image: CardImage) -> CardImage:
        """
        Update existing card image.
        
        Args:
            image: CardImage entity with updates
            
        Returns:
            Updated CardImage
        """
        db_image = self.session.query(CardImageModel).filter(
            CardImageModel.id == image.id
        ).first()
        
        if not db_image:
            raise ValueError(f"Image with ID {image.id} not found")
        
        # Update fields
        db_image.status = image.status.value
        db_image.card_id = image.card_id
        db_image.processed_at = image.processed_at
        db_image.error_message = image.error_message
        
        self.session.commit()
        self.session.refresh(db_image)
        
        logger.info(f"Updated image ID: {db_image.id}")
        
        return self._to_entity(db_image)
    
    async def delete(self, image_id: int) -> bool:
        """
        Delete card image by ID.
        
        Args:
            image_id: Image ID
            
        Returns:
            True if deleted, False if not found
        """
        db_image = self.session.query(CardImageModel).filter(
            CardImageModel.id == image_id
        ).first()
        
        if not db_image:
            return False
        
        self.session.delete(db_image)
        self.session.commit()
        
        logger.info(f"Deleted image ID: {image_id}")
        
        return True
    
    def _to_entity(self, db_image: CardImageModel) -> CardImage:
        """
        Convert ORM model to domain entity.
        
        Args:
            db_image: SQLAlchemy ORM model
            
        Returns:
            CardImage domain entity
        """
        return CardImage(
            id=db_image.id,
            original_path=db_image.original_path,
            status=ImageStatus(db_image.status),
            card_id=db_image.card_id,
            created_at=db_image.created_at,
            processed_at=db_image.processed_at,
            error_message=db_image.error_message
        )
