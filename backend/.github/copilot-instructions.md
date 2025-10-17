# GitHub Copilot Instructions - Backend (Python/FastAPI)

## 🐍 Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── cards.py         # Card CRUD endpoints
│   │   ├── images.py        # Image upload endpoints
│   │   └── ocr.py           # OCR processing endpoints
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py        # Settings and environment variables
│   │   └── database.py      # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── card.py          # Card model
│   │   └── card_image.py    # CardImage model
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── card.py          # Card schemas
│   │   └── image.py         # Image schemas
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── ocr_service.py   # OCR with Groq API
│   │   └── storage.py       # Image storage
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── logger.py        # Logging configuration
├── tests/                   # Unit and integration tests
├── requirements.txt
└── Dockerfile
```

---

## 🎨 Python Conventions

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

## ✅ Testing

### Test Structure
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
