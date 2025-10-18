"""Image status enum."""
from enum import Enum


class ImageStatus(str, Enum):
    """Status of an uploaded image in the OCR workflow."""
    
    NON_TRAITE = "non_traite"
    EN_COURS = "en_cours"
    ATTENTE_VALIDATION = "attente_validation"
    VALIDE = "valide"
    ERROR = "error"
