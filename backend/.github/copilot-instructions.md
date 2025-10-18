# GitHub Copilot Instructions - Backend (Python/FastAPI)

## 🐍 Backend Structure (Clean Architecture)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app initialization
│   │
│   ├── api/                       # 🎯 PRESENTATION LAYER (Controllers)
│   │   ├── __init__.py
│   │   ├── dependencies.py        # Dependency injection
│   │   ├── cards.py               # Card endpoints
│   │   ├── images.py              # Image upload endpoints
│   │   └── ocr.py                 # OCR processing endpoints
│   │
│   ├── core/                      # 🔧 INFRASTRUCTURE (Config, DB)
│   │   ├── __init__.py
│   │   ├── config.py              # Settings and environment variables
│   │   └── database.py            # Database connection
│   │
│   ├── domain/                    # 🏛️ DOMAIN LAYER (Business entities)
│   │   ├── __init__.py
│   │   ├── entities/              # Domain entities (pure Python)
│   │   │   ├── __init__.py
│   │   │   ├── card.py            # Card entity
│   │   │   └── card_image.py      # CardImage entity
│   │   └── enums/                 # Domain enums
│   │       ├── __init__.py
│   │       ├── encre.py           # Ink color enum
│   │       ├── rarete.py          # Rarity enum
│   │       └── status.py          # Status enum
│   │
│   ├── application/               # 💼 APPLICATION LAYER (Use Cases)
│   │   ├── __init__.py
│   │   ├── use_cases/             # Business logic orchestration
│   │   │   ├── __init__.py
│   │   │   ├── upload_card_image.py
│   │   │   ├── process_ocr.py
│   │   │   ├── validate_card.py
│   │   │   ├── get_card.py
│   │   │   └── list_cards.py
│   │   └── interfaces/            # Abstract interfaces (Ports)
│   │       ├── __init__.py
│   │       ├── card_repository.py # Card repo interface
│   │       ├── image_repository.py
│   │       ├── ocr_service.py     # OCR service interface
│   │       └── storage_service.py # Storage interface
│   │
│   ├── infrastructure/            # 🔌 INFRASTRUCTURE LAYER (Adapters)
│   │   ├── __init__.py
│   │   ├── database/              # Database implementations
│   │   │   ├── __init__.py
│   │   │   ├── models/            # SQLAlchemy models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── card.py
│   │   │   │   └── card_image.py
│   │   │   └── repositories/      # Repository implementations
│   │   │       ├── __init__.py
│   │   │       ├── card_repository.py
│   │   │       └── image_repository.py
│   │   ├── external/              # External services
│   │   │   ├── __init__.py
│   │   │   ├── groq_ocr_service.py # Groq API implementation
│   │   │   └── local_storage.py    # Local file storage
│   │   └── logging/               # Logging infrastructure
│   │       ├── __init__.py
│   │       └── logger.py
│   │
│   └── schemas/                   # 📋 DTOs (Pydantic schemas)
│       ├── __init__.py
│       ├── card.py                # Card DTOs
│       ├── image.py               # Image DTOs
│       └── ocr.py                 # OCR DTOs
│
├── tests/                         # Unit and integration tests
├── requirements.txt
└── Dockerfile
```

### 🏗️ Clean Architecture Layers

1. **Domain Layer** (Innermost): Business entities, value objects, domain logic
2. **Application Layer**: Use cases, business logic orchestration, interfaces
3. **Infrastructure Layer**: External services, database, file system
4. **Presentation Layer** (Outermost): API endpoints, request/response handling

**Dependency Rule**: Dependencies point INWARD. Outer layers depend on inner layers, never the reverse.

---

## � SOLID Principles

### Single Responsibility Principle (SRP)
Each class/module has ONE reason to change.

```python
# ❌ BAD: Class doing too many things
class CardService:
    def create_card(self, data):
        # Validate data
        # Save to database
        # Send notification
        # Log activity
        pass

# ✅ GOOD: Separate responsibilities
class CardValidator:
    def validate(self, data: CardCreate) -> bool:
        """Only validates card data."""
        pass

class CardRepository:
    def save(self, card: Card) -> Card:
        """Only handles database operations."""
        pass

class CreateCardUseCase:
    def __init__(self, validator: CardValidator, repository: CardRepository):
        self.validator = validator
        self.repository = repository
    
    def execute(self, data: CardCreate) -> Card:
        """Orchestrates card creation."""
        self.validator.validate(data)
        return self.repository.save(data)
```

### Open/Closed Principle (OCP)
Open for extension, closed for modification.

```python
# Use ABC for extensibility
from abc import ABC, abstractmethod

class OCRService(ABC):
    @abstractmethod
    async def extract_card_info(self, image_path: Path) -> Optional[CardInfo]:
        """Extract card information from image."""
        pass

# Extend without modifying base
class GroqOCRService(OCRService):
    async def extract_card_info(self, image_path: Path) -> Optional[CardInfo]:
        # Groq-specific implementation
        pass

class TesseractOCRService(OCRService):
    async def extract_card_info(self, image_path: Path) -> Optional[CardInfo]:
        # Tesseract-specific implementation
        pass
```

### Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types.

```python
# Repository interface
class ICardRepository(ABC):
    @abstractmethod
    def get_by_id(self, card_id: int) -> Optional[Card]:
        pass

# Can swap implementations without breaking code
class SQLAlchemyCardRepository(ICardRepository):
    def get_by_id(self, card_id: int) -> Optional[Card]:
        return self.session.query(Card).get(card_id)

class InMemoryCardRepository(ICardRepository):
    def get_by_id(self, card_id: int) -> Optional[Card]:
        return self.cards.get(card_id)
```

### Interface Segregation Principle (ISP)
Clients shouldn't depend on interfaces they don't use.

```python
# ❌ BAD: Fat interface
class IRepository(ABC):
    @abstractmethod
    def create(self): pass
    @abstractmethod
    def read(self): pass
    @abstractmethod
    def update(self): pass
    @abstractmethod
    def delete(self): pass
    @abstractmethod
    def search(self): pass
    @abstractmethod
    def export(self): pass

# ✅ GOOD: Segregated interfaces
class IReadRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int): pass
    @abstractmethod
    def list_all(self): pass

class IWriteRepository(ABC):
    @abstractmethod
    def save(self, entity): pass
    @abstractmethod
    def delete(self, id: int): pass

class ISearchRepository(ABC):
    @abstractmethod
    def search(self, criteria): pass
```

### Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions.

```python
# ❌ BAD: Direct dependency on concrete class
class ProcessOCRUseCase:
    def __init__(self):
        self.ocr_service = GroqOCRService()  # Tight coupling!
    
    def execute(self, image_path: Path):
        return self.ocr_service.extract_card_info(image_path)

# ✅ GOOD: Depend on abstraction
class ProcessOCRUseCase:
    def __init__(self, ocr_service: OCRService):  # Interface!
        self.ocr_service = ocr_service
    
    def execute(self, image_path: Path):
        return self.ocr_service.extract_card_info(image_path)

# Dependency injection in FastAPI
def get_ocr_service() -> OCRService:
    return GroqOCRService(api_key=settings.GROQ_API_KEY)

@router.post("/process")
async def process_ocr(
    image_id: int,
    ocr_service: OCRService = Depends(get_ocr_service)
):
    use_case = ProcessOCRUseCase(ocr_service)
    return use_case.execute(image_id)
```

---

## �🎨 Python Conventions

### Type Hints
Always use type hints for function parameters and return values:

```python
from typing import Optional, List
from pydantic import BaseModel

def get_card(card_id: int) -> Optional[Card]:
    """Get a card by ID."""
    pass

async def list_cards(skip: int = 0, limit: int = 100) -> List[Card]:
    """List cards with pagination."""
    pass
```

### Docstrings
Use Google-style docstrings:

```python
def process_ocr(image_path: str, api_key: str) -> Optional[CardInfo]:
    """
    Extract card information from an image using OCR.

    Args:
        image_path: Path to the card image
        api_key: Groq API key for OCR

    Returns:
        Extracted card information or None if processing fails

    Raises:
        ValueError: If image format is invalid
        APIError: If OCR API call fails
    """
    pass
```

### Error Handling
Use specific exceptions and log errors:

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

try:
    result = process_ocr(image_path, api_key)
except ValueError as e:
    logger.error(f"Invalid image format: {e}")
    raise HTTPException(status_code=400, detail="Invalid image format")
except Exception as e:
    logger.error(f"OCR processing failed: {e}")
    raise HTTPException(status_code=500, detail="OCR processing failed")
```

---

## 🏛️ Clean Architecture Patterns

### Domain Entities (Pure Python)
```python
# domain/entities/card.py
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Card:
    """Pure domain entity - no framework dependencies."""
    nom: str
    encre: Optional[str]
    cout: Optional[int]
    force: Optional[int]
    volonte: Optional[int]
    lore: Optional[int]
    rarete: Optional[str]
    texte: Optional[str]
    mots_cles: List[str]
    encrable: bool
    status: str = "attente_validation"
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def validate(self) -> bool:
        """Domain validation logic."""
        if not self.nom or len(self.nom) == 0:
            raise ValueError("Card name is required")
        if self.cout and (self.cout < 0 or self.cout > 20):
            raise ValueError("Cost must be between 0 and 20")
        return True
```

### Use Cases (Application Layer)
```python
# application/use_cases/create_card.py
from typing import Optional
from app.domain.entities.card import Card
from app.application.interfaces.card_repository import ICardRepository

class CreateCardUseCase:
    """Use case: Create a new card (Application logic)."""
    
    def __init__(self, card_repository: ICardRepository):
        self.card_repository = card_repository
    
    async def execute(self, card_data: dict) -> Card:
        """
        Execute the create card use case.
        
        Args:
            card_data: Raw card data from request
            
        Returns:
            Created card entity
            
        Raises:
            ValueError: If validation fails
        """
        # 1. Create domain entity
        card = Card(**card_data)
        
        # 2. Validate (domain logic)
        card.validate()
        
        # 3. Persist (through repository interface)
        saved_card = await self.card_repository.save(card)
        
        return saved_card
```

### Repository Interface (Application Layer)
```python
# application/interfaces/card_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.card import Card

class ICardRepository(ABC):
    """Repository interface (Port) - defines contract."""
    
    @abstractmethod
    async def save(self, card: Card) -> Card:
        """Persist a card."""
        pass
    
    @abstractmethod
    async def get_by_id(self, card_id: int) -> Optional[Card]:
        """Retrieve card by ID."""
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Card]:
        """List all cards with pagination."""
        pass
    
    @abstractmethod
    async def update(self, card: Card) -> Card:
        """Update existing card."""
        pass
    
    @abstractmethod
    async def delete(self, card_id: int) -> bool:
        """Delete card by ID."""
        pass
```

### Repository Implementation (Infrastructure Layer)
```python
# infrastructure/database/repositories/card_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.application.interfaces.card_repository import ICardRepository
from app.domain.entities.card import Card
from app.infrastructure.database.models.card import CardModel

class SQLAlchemyCardRepository(ICardRepository):
    """SQLAlchemy implementation of card repository (Adapter)."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def save(self, card: Card) -> Card:
        """Save card to database."""
        # Convert domain entity to ORM model
        db_card = CardModel(
            nom=card.nom,
            encre=card.encre,
            cout=card.cout,
            # ... other fields
        )
        self.session.add(db_card)
        self.session.commit()
        self.session.refresh(db_card)
        
        # Convert ORM model back to domain entity
        return self._to_entity(db_card)
    
    async def get_by_id(self, card_id: int) -> Optional[Card]:
        """Get card by ID."""
        db_card = self.session.query(CardModel).filter(CardModel.id == card_id).first()
        return self._to_entity(db_card) if db_card else None
    
    def _to_entity(self, db_card: CardModel) -> Card:
        """Convert ORM model to domain entity."""
        return Card(
            id=db_card.id,
            nom=db_card.nom,
            encre=db_card.encre,
            # ... other fields
        )
```

### API Endpoint (Presentation Layer)
```python
# api/cards.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.card import CardCreateDTO, CardResponseDTO
from app.application.use_cases.create_card import CreateCardUseCase
from app.infrastructure.database.repositories.card_repository import SQLAlchemyCardRepository

router = APIRouter(prefix="/api/cards", tags=["cards"])

def get_card_repository(db: Session = Depends(get_db)) -> SQLAlchemyCardRepository:
    """Dependency: Card repository."""
    return SQLAlchemyCardRepository(db)

@router.post("/", response_model=CardResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_card(
    card_data: CardCreateDTO,
    repository: SQLAlchemyCardRepository = Depends(get_card_repository)
) -> CardResponseDTO:
    """
    Create a new card.
    
    This endpoint receives card data, validates it, and persists it.
    """
    try:
        # Instantiate use case with repository
        use_case = CreateCardUseCase(repository)
        
        # Execute business logic
        card = await use_case.execute(card_data.dict())
        
        # Return DTO (not domain entity!)
        return CardResponseDTO.from_entity(card)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### DTOs (Data Transfer Objects)
```python
# schemas/card.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.domain.entities.card import Card

class CardCreateDTO(BaseModel):
    """DTO for creating a card (input)."""
    nom: str = Field(..., min_length=1, max_length=100)
    encre: Optional[str] = None
    cout: Optional[int] = Field(None, ge=0, le=20)
    force: Optional[int] = None
    volonte: Optional[int] = None
    lore: Optional[int] = None
    rarete: Optional[str] = None
    texte: Optional[str] = None
    mots_cles: List[str] = []
    encrable: bool = False

class CardResponseDTO(BaseModel):
    """DTO for card response (output)."""
    id: int
    nom: str
    encre: Optional[str]
    cout: Optional[int]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True
    
    @classmethod
    def from_entity(cls, entity: Card) -> "CardResponseDTO":
        """Convert domain entity to DTO."""
        return cls(
            id=entity.id,
            nom=entity.nom,
            encre=entity.encre,
            cout=entity.cout,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
```

---

## 🔧 FastAPI Patterns

### Endpoint Structure
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.card import CardCreate, CardResponse
from app.services import card_service

router = APIRouter(prefix="/api/cards", tags=["cards"])

@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def create_card(
    card: CardCreate,
    db: Session = Depends(get_db)
) -> CardResponse:
    """Create a new card."""
    return card_service.create(db, card)
```

### Dependency Injection
```python
from app.core.config import settings

def get_ocr_service():
    """Dependency for OCR service."""
    return OCRService(api_key=settings.GROQ_API_KEY)
```

---

## 📦 Pydantic Models

### Schema Best Practices
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class CardBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    encre: Optional[str] = Field(None, regex="^(Amber|Amethyst|Emerald|Ruby|Sapphire|Steel)$")
    cout: Optional[int] = Field(None, ge=0, le=20)
    
    @validator('mots_cles')
    def validate_keywords(cls, v):
        """Ensure keywords are not empty strings."""
        return [k.strip() for k in v if k.strip()]

class CardCreate(CardBase):
    """Schema for creating a card."""
    pass

class CardResponse(CardBase):
    """Schema for card response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

---

## 🗄️ SQLAlchemy Models

### Model Best Practices
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, index=True)
    encre = Column(String(20), index=True)
    cout = Column(Integer)
    force = Column(Integer)
    volonte = Column(Integer)
    lore = Column(Integer)
    rarete = Column(String(20), index=True)
    status = Column(String(20), default="attente_validation", index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    images = relationship("CardImage", back_populates="card")
```

---

## 🔍 OCR Service Pattern

### Reuse from lorcana_price
Adapt the OCR logic from `fill_sheet_with_ocr.py`:

```python
import base64
from groq import Groq
from pathlib import Path

class OCRService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    def encode_image(self, image_path: Path) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    async def extract_card_info(self, image_path: Path) -> Optional[CardInfo]:
        """Extract card information using Groq API."""
        # Reuse the optimized prompt from fill_sheet_with_ocr.py
        pass
```

---

## 📝 Logging

### Logger Configuration
```python
import logging

def setup_logger(name: str) -> logging.Logger:
    """Configure logger with consistent format."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage
logger = setup_logger(__name__)
logger.info("Card created successfully")
logger.error(f"Failed to process OCR: {error}")
```

---

## ⚠️ Error Handling & Exceptions

### Custom Domain Exceptions
```python
# domain/exceptions.py
class DomainException(Exception):
    """Base exception for domain errors."""
    pass

class CardValidationError(DomainException):
    """Raised when card validation fails."""
    pass

class CardNotFoundError(DomainException):
    """Raised when card is not found."""
    pass

class OCRProcessingError(DomainException):
    """Raised when OCR processing fails."""
    pass
```

### Exception Handling in Use Cases
```python
# application/use_cases/get_card.py
class GetCardUseCase:
    def __init__(self, repository: ICardRepository):
        self.repository = repository
    
    async def execute(self, card_id: int) -> Card:
        """Get card by ID."""
        card = await self.repository.get_by_id(card_id)
        
        if not card:
            raise CardNotFoundError(f"Card with ID {card_id} not found")
        
        return card
```

### Exception Handling in API Layer
```python
# api/cards.py
from app.domain.exceptions import CardNotFoundError, CardValidationError

@router.get("/{card_id}")
async def get_card(
    card_id: int,
    repository: ICardRepository = Depends(get_card_repository)
):
    """Get card by ID."""
    try:
        use_case = GetCardUseCase(repository)
        card = await use_case.execute(card_id)
        return CardResponseDTO.from_entity(card)
    
    except CardNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except CardValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error getting card {card_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## ✅ Testing

### Test Structure (Clean Architecture)
```python
# tests/unit/domain/test_card_entity.py
"""Test domain entities (no dependencies)."""
import pytest
from app.domain.entities.card import Card

def test_card_validation_success():
    """Test valid card creation."""
    card = Card(
        nom="Mickey Mouse",
        encre="Amber",
        cout=3,
        mots_cles=["Hero", "Dreamborn"],
        encrable=True
    )
    assert card.validate() is True

def test_card_validation_empty_name():
    """Test card validation with empty name."""
    card = Card(nom="", encre="Amber", cout=3, mots_cles=[], encrable=False)
    
    with pytest.raises(ValueError, match="Card name is required"):
        card.validate()

# tests/unit/application/test_create_card_use_case.py
"""Test use cases with mocked dependencies."""
import pytest
from unittest.mock import Mock, AsyncMock
from app.application.use_cases.create_card import CreateCardUseCase
from app.domain.entities.card import Card

@pytest.mark.asyncio
async def test_create_card_use_case_success():
    """Test create card use case with valid data."""
    # Arrange
    mock_repository = Mock()
    mock_repository.save = AsyncMock(return_value=Card(
        id=1, nom="Test Card", encre="Amber", cout=3, 
        mots_cles=[], encrable=False
    ))
    
    use_case = CreateCardUseCase(mock_repository)
    
    # Act
    result = await use_case.execute({
        "nom": "Test Card",
        "encre": "Amber",
        "cout": 3,
        "mots_cles": [],
        "encrable": False
    })
    
    # Assert
    assert result.id == 1
    assert result.nom == "Test Card"
    mock_repository.save.assert_called_once()

# tests/integration/test_card_repository.py
"""Test repository implementations with real database."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.repositories.card_repository import SQLAlchemyCardRepository
from app.domain.entities.card import Card

@pytest.fixture
def db_session():
    """Create test database session."""
    engine = create_engine("sqlite:///:memory:")
    # Create tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.mark.asyncio
async def test_card_repository_save(db_session):
    """Test saving card to database."""
    repository = SQLAlchemyCardRepository(db_session)
    
    card = Card(nom="Test", encre="Amber", cout=3, mots_cles=[], encrable=False)
    saved_card = await repository.save(card)
    
    assert saved_card.id is not None
    assert saved_card.nom == "Test"

# tests/e2e/test_card_api.py
"""End-to-end API tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_card_endpoint():
    """Test card creation endpoint."""
    response = client.post(
        "/api/cards/",
        json={
            "nom": "Mickey Mouse",
            "encre": "Amber",
            "cout": 3,
            "mots_cles": ["Hero"],
            "encrable": True
        }
    )
    assert response.status_code == 201
    assert response.json()["nom"] == "Mickey Mouse"

def test_get_card_not_found():
    """Test getting non-existent card."""
    response = client.get("/api/cards/99999")
    assert response.status_code == 404
```

---

## 📚 Best Practices Summary

### ✅ DO
- **Separate concerns**: Domain, Application, Infrastructure, Presentation
- **Use interfaces**: Define contracts in application layer
- **Inject dependencies**: Never instantiate dependencies inside classes
- **Test in isolation**: Mock dependencies for unit tests
- **Validate in domain**: Business rules belong in entities
- **Use DTOs**: Don't expose domain entities in API
- **Handle errors gracefully**: Custom exceptions, proper HTTP codes
- **Log everything**: Use structured logging
- **Type everything**: Use type hints everywhere

### ❌ DON'T
- **Mix layers**: Don't put business logic in controllers
- **Depend on concretions**: Always depend on abstractions
- **Expose internals**: Don't return ORM models in API
- **Skip validation**: Always validate input
- **Ignore errors**: Handle all exceptions appropriately
- **Use print()**: Use proper logging
- **Couple to frameworks**: Keep domain pure Python
- **Skip tests**: Test all layers separately

---

## 🎯 Implementation Checklist

When implementing a new feature:

1. ✅ **Define domain entity** (pure Python dataclass)
2. ✅ **Create repository interface** (in application/interfaces)
3. ✅ **Implement use case** (business logic orchestration)
4. ✅ **Create DTOs** (Pydantic schemas for API)
5. ✅ **Implement repository** (SQLAlchemy in infrastructure)
6. ✅ **Create API endpoint** (FastAPI controller)
7. ✅ **Add dependency injection** (in api/dependencies.py)
8. ✅ **Write tests** (unit → integration → e2e)
9. ✅ **Add logging** (at all layers)
10. ✅ **Document** (docstrings + OpenAPI)

---

## ✅ Testing (Original Section Preserved)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_card():
    """Test card creation endpoint."""
    response = client.post(
        "/api/cards/",
        json={"nom": "Test Card", "encre": "Amber", "cout": 3}
    )
    assert response.status_code == 201
    assert response.json()["nom"] == "Test Card"

@pytest.mark.asyncio
async def test_ocr_service():
    """Test OCR extraction."""
    service = OCRService(api_key="test_key")
    # Mock Groq API response
    pass
```

---

## 🔑 Environment Variables

### Configuration Pattern
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API
    GROQ_API_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./lorcana_cards.db"
    
    # Storage
    UPLOAD_FOLDER: str = "/app/uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:4200"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🚀 Common Patterns

### Pagination
```python
from fastapi import Query

@router.get("/")
async def list_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List cards with pagination."""
    cards = db.query(Card).offset(skip).limit(limit).all()
    total = db.query(Card).count()
    return {"items": cards, "total": total, "skip": skip, "limit": limit}
```

### File Upload
```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    storage: StorageService = Depends(get_storage)
):
    """Upload card image."""
    # Validate file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(400, "Invalid file type")
    
    # Save file
    file_path = await storage.save(file)
    return {"file_path": str(file_path)}
```
