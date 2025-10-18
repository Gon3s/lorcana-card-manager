"""Card model - Stores Lorcana card information."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Index
from sqlalchemy.orm import relationship

from .base import Base


class Card(Base):
    """
    Represents a Lorcana card with all its attributes.
    
    Attributes:
        id: Primary key
        nom: Card name
        sous_titre: Card subtitle
        encre: Ink color (Amber, Amethyst, Emerald, Ruby, Sapphire, Steel)
        encrable: Whether the card is inkable
        cout: Ink cost
        force: Strength value (for characters)
        volonte: Willpower value (for characters)
        lore: Lore value
        mots_cles: Keywords (comma-separated or JSON)
        texte: Card ability text (original language)
        texte_fr: Card ability text (French translation)
        rarete: Rarity (Common, Uncommon, Rare, Super Rare, Legendary, Enchanted)
        image_path: Path to the card image file
        status: Current status (attente_validation, valide)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "cards"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Card information
    nom = Column(String(255), nullable=False, index=True)
    sous_titre = Column(String(255), nullable=True)
    encre = Column(String(50), nullable=False, index=True)  # Amber, Amethyst, etc.
    encrable = Column(Boolean, default=False, nullable=False)
    cout = Column(Integer, nullable=True)
    force = Column(Integer, nullable=True)
    volonte = Column(Integer, nullable=True)
    lore = Column(Integer, nullable=True)
    mots_cles = Column(Text, nullable=True)  # JSON array or comma-separated
    texte = Column(Text, nullable=True)
    texte_fr = Column(Text, nullable=True)
    rarete = Column(String(50), nullable=False, index=True)
    
    # Image & metadata
    image_path = Column(String(500), nullable=True)
    status = Column(
        String(50), 
        nullable=False, 
        default="attente_validation",
        index=True
    )  # attente_validation, valide
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    card_images = relationship("CardImage", back_populates="card", cascade="all, delete-orphan")
    
    # Indexes for frequent queries
    __table_args__ = (
        Index("idx_card_search", "nom", "encre", "rarete"),
        Index("idx_card_status_created", "status", "created_at"),
    )
    
    def __repr__(self):
        return f"<Card(id={self.id}, nom='{self.nom}', encre='{self.encre}', status='{self.status}')>"
