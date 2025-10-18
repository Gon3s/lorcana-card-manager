"""Card domain entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from app.domain.enums import Encre, Rarete, CardStatus


@dataclass
class Card:
    """
    Domain entity representing a Lorcana card.
    
    This is a pure Python object with no framework dependencies.
    Contains business logic and validation rules.
    """
    
    nom: str
    mots_cles: List[str] = field(default_factory=list)
    encrable: bool = False
    
    # Optional fields
    sous_titre: Optional[str] = None
    encre: Optional[Encre] = None
    cout: Optional[int] = None
    force: Optional[int] = None
    volonte: Optional[int] = None
    lore: Optional[int] = None
    rarete: Optional[Rarete] = None
    texte: Optional[str] = None
    texte_fr: Optional[str] = None
    image_path: Optional[str] = None
    
    # Status and metadata
    status: CardStatus = CardStatus.ATTENTE_VALIDATION
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def validate(self) -> bool:
        """
        Validate the card entity according to business rules.
        
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.nom or len(self.nom.strip()) == 0:
            raise ValueError("Card name is required")
        
        if self.cout is not None and (self.cout < 0 or self.cout > 20):
            raise ValueError("Cost must be between 0 and 20")
        
        if self.force is not None and self.force < 0:
            raise ValueError("Force cannot be negative")
        
        if self.volonte is not None and self.volonte < 0:
            raise ValueError("Volonte (Willpower) cannot be negative")
        
        if self.lore is not None and self.lore < 0:
            raise ValueError("Lore cannot be negative")
        
        return True
    
    def mark_validated(self) -> None:
        """Mark card as validated."""
        self.status = CardStatus.VALIDE
        self.updated_at = datetime.now()
    
    def archive(self) -> None:
        """Archive the card."""
        self.status = CardStatus.ARCHIVED
        self.updated_at = datetime.now()
    
    def is_character(self) -> bool:
        """Check if card is a character (has force/volonte)."""
        return self.force is not None or self.volonte is not None
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Card(id={self.id}, nom={self.nom}, encre={self.encre}, status={self.status.value})"
