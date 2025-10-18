"""OCRLog model - Stores OCR processing history and results."""

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


class OCRLog(Base):
    """
    Stores the history of OCR processing attempts for each card image.
    
    This table keeps track of all OCR attempts, successful or failed,
    for debugging and auditing purposes.
    
    Attributes:
        id: Primary key
        card_image_id: Foreign key to card_images table
        raw_response: Raw JSON response from Groq API
        error_message: Error message if OCR failed
        created_at: Processing timestamp
    """
    
    __tablename__ = "ocr_logs"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign key
    card_image_id = Column(Integer, ForeignKey("card_images.id"), nullable=False, index=True)
    
    # OCR data
    raw_response = Column(Text, nullable=True)  # JSON response from Groq
    error_message = Column(Text, nullable=True)  # Error details if failed
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    card_image = relationship("CardImage", back_populates="ocr_logs")
    
    # Index for querying logs by image
    __table_args__ = (
        Index("idx_ocr_image_created", "card_image_id", "created_at"),
    )
    
    def __repr__(self):
        return f"<OCRLog(id={self.id}, card_image_id={self.card_image_id}, has_error={bool(self.error_message)})>"
