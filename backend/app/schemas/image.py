"""Image DTOs for API requests and responses."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.entities.card_image import CardImage
from app.domain.enums import ImageStatus


class ImageResponseDTO(BaseModel):
    """DTO for image response (output)."""
    
    id: int
    original_path: str
    status: ImageStatus
    card_id: Optional[int] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        from_attributes = True
        use_enum_values = True
    
    @classmethod
    def from_entity(cls, entity: CardImage) -> "ImageResponseDTO":
        """
        Convert domain entity to DTO.
        
        Args:
            entity: CardImage domain entity
            
        Returns:
            ImageResponseDTO
        """
        return cls(
            id=entity.id,
            original_path=entity.original_path,
            status=entity.status,
            card_id=entity.card_id,
            created_at=entity.created_at,
            processed_at=entity.processed_at,
            error_message=entity.error_message
        )


class ImageUploadResponseDTO(BaseModel):
    """DTO for successful upload response."""
    
    image_id: int
    status: ImageStatus
    message: str = "Image uploaded successfully"
    
    class Config:
        """Pydantic config."""
        use_enum_values = True
