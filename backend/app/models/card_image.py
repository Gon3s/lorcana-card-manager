"""CardImage model - Tracks uploaded images and their processing status."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


class CardImage(Base):
    """
    Represents an uploaded card image and its processing status.
    
    Status workflow:
        non_traite -> en_cours -> attente_validation -> valide
    
    Attributes:
        id: Primary key
        card_id: Foreign key to cards table (nullable until validated)
        original_path: Path to the uploaded image file
        status: Processing status
        created_at: Upload timestamp
    """
    
    __tablename__ = "card_images"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign key (nullable until card is created and validated)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=True, index=True)
    
    # Image information
    original_path = Column(String(500), nullable=False)
    
    # Status tracking
    status = Column(
        String(50), 
        nullable=False, 
        default="non_traite",
        index=True
    )  # non_traite, en_cours, attente_validation, valide
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    card = relationship("Card", back_populates="card_images")
    ocr_logs = relationship("OCRLog", back_populates="card_image", cascade="all, delete-orphan")
    
    # Index for status queries
    __table_args__ = (
        Index("idx_image_status_created", "status", "created_at"),
    )
    
    def __repr__(self):
        return f"<CardImage(id={self.id}, status='{self.status}', card_id={self.card_id})>"
