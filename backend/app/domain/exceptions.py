"""Domain-specific exceptions."""


class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class CardValidationError(DomainException):
    """Raised when card validation fails."""
    pass


class CardNotFoundError(DomainException):
    """Raised when card is not found."""
    pass


class ImageValidationError(DomainException):
    """Raised when image validation fails."""
    pass


class ImageNotFoundError(DomainException):
    """Raised when image is not found."""
    pass


class OCRProcessingError(DomainException):
    """Raised when OCR processing fails."""
    pass


class StorageError(DomainException):
    """Raised when file storage operation fails."""
    pass
