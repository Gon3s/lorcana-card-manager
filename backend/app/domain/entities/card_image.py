"""CardImage domain entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from pathlib import Path

from app.domain.enums import ImageStatus


@dataclass
class CardImage:
    """
    Domain entity representing a card image.
    
    This is a pure Python object with no framework dependencies.
    Contains business logic related to card images.
    """
    
    original_path: str
    status: ImageStatus = ImageStatus.NON_TRAITE
    card_id: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def validate(self) -> bool:
        """
        Validate the card image entity.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.original_path:
            raise ValueError("Image path is required")
        
        # Check file extension
        path = Path(self.original_path)
        if path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            raise ValueError("Invalid image format. Only JPG and PNG are supported")
        
        return True
    
    def mark_processing(self) -> None:
        """Mark image as being processed."""
        self.status = ImageStatus.EN_COURS
    
    def mark_awaiting_validation(self) -> None:
        """Mark image as awaiting validation after OCR."""
        self.status = ImageStatus.ATTENTE_VALIDATION
        self.processed_at = datetime.now()
    
    def mark_validated(self, card_id: int) -> None:
        """
        Mark image as validated and link to card.
        
        Args:
            card_id: ID of the validated card
        """
        self.status = ImageStatus.VALIDE
        self.card_id = card_id
    
    def mark_error(self, error_message: str) -> None:
        """
        Mark image as errored.
        
        Args:
            error_message: Description of the error
        """
        self.status = ImageStatus.ERROR
        self.error_message = error_message
        self.processed_at = datetime.now()
    
    def is_processable(self) -> bool:
        """Check if image can be processed by OCR."""
        return self.status in [ImageStatus.NON_TRAITE, ImageStatus.ERROR]
    
    def __repr__(self) -> str:
        """String representation."""
        return f"CardImage(id={self.id}, path={self.original_path}, status={self.status.value})"
