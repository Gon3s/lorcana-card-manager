"""Image repository interface (Port)."""
from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.card_image import CardImage
from app.domain.enums import ImageStatus


class IImageRepository(ABC):
    """
    Repository interface for CardImage entities.
    
    This is a Port in Clean Architecture - defines the contract
    without implementation details.
    """
    
    @abstractmethod
    async def save(self, image: CardImage) -> CardImage:
        """
        Persist a card image.
        
        Args:
            image: CardImage entity to save
            
        Returns:
            Saved CardImage with ID
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, image_id: int) -> Optional[CardImage]:
        """
        Retrieve card image by ID.
        
        Args:
            image_id: Image ID
            
        Returns:
            CardImage entity or None if not found
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def update(self, image: CardImage) -> CardImage:
        """
        Update existing card image.
        
        Args:
            image: CardImage entity with updates
            
        Returns:
            Updated CardImage
        """
        pass
    
    @abstractmethod
    async def delete(self, image_id: int) -> bool:
        """
        Delete card image by ID.
        
        Args:
            image_id: Image ID
            
        Returns:
            True if deleted, False if not found
        """
        pass
