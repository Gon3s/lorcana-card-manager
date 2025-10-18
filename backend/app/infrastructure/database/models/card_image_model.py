"""CardImage ORM model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class CardImageModel(Base):
    """
    SQLAlchemy ORM model for card_images table.
    
    This is an infrastructure concern - maps to database structure.
    Separate from domain entity (CardImage).
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
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    
    # Relationships
    card = relationship("Card", back_populates="card_images")
    ocr_logs = relationship("OCRLog", back_populates="card_image", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index("idx_image_status_created", "status", "created_at"),
    )
    
    def __repr__(self):
        return f"<CardImageModel(id={self.id}, status='{self.status}')>"
