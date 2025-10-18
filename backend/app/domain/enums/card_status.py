"""Card status enum."""
from enum import Enum


class CardStatus(str, Enum):
    """Status of a card in the system."""
    
    ATTENTE_VALIDATION = "attente_validation"
    VALIDE = "valide"
    ARCHIVED = "archived"
