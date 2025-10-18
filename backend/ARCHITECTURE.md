# 🏗️ Architecture Backend - Lorcana Card Manager

## 📐 Clean Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│                    (FastAPI Endpoints)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              APPLICATION LAYER                      │   │
│  │              (Use Cases + Interfaces)               │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │          DOMAIN LAYER                       │   │   │
│  │  │      (Entities, Value Objects)              │   │   │
│  │  │                                             │   │   │
│  │  │  - Card (entity)                            │   │   │
│  │  │  - CardImage (entity)                       │   │   │
│  │  │  - Encre, Rarete, Status (enums)            │   │   │
│  │  │                                             │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                     │   │
│  │  - CreateCardUseCase                                │   │
│  │  - ProcessOCRUseCase                                │   │
│  │  - ValidateCardUseCase                              │   │
│  │  - ICardRepository (interface)                      │   │
│  │  - IOCRService (interface)                          │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  - POST /api/cards                                          │
│  - GET /api/cards/{id}                                      │
│  - POST /api/images/upload                                  │
│  - POST /api/ocr/process                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                       │
│                  (External Concerns)                        │
│                                                             │
│  Database:                                                  │
│  - SQLAlchemyCardRepository (implements ICardRepository)    │
│  - CardModel, CardImageModel (SQLAlchemy ORM)               │
│                                                             │
│  External Services:                                         │
│  - GroqOCRService (implements IOCRService)                  │
│  - LocalStorageService (file system)                        │
│                                                             │
│  Logging:                                                   │
│  - StructuredLogger                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 SOLID Principles Quick Reference

| Principle | What it means | Example |
|-----------|---------------|---------|
| **S**ingle Responsibility | One class, one job | `CardValidator` only validates, `CardRepository` only persists |
| **O**pen/Closed | Open for extension, closed for modification | Use `OCRService` interface, extend with `GroqOCRService` |
| **L**iskov Substitution | Subtypes can replace base types | Any `ICardRepository` implementation works |
| **I**nterface Segregation | Small, focused interfaces | `IReadRepository` vs `IWriteRepository` |
| **D**ependency Inversion | Depend on abstractions | Inject `IOCRService`, not `GroqOCRService` |

## 📁 Directory Structure

```
backend/app/
│
├── domain/                    # 🏛️ CORE BUSINESS LOGIC (no dependencies)
│   ├── entities/              # Business entities (Card, CardImage)
│   ├── enums/                 # Domain enums (Encre, Rarete, Status)
│   └── exceptions.py          # Domain-specific exceptions
│
├── application/               # 💼 USE CASES & CONTRACTS
│   ├── use_cases/             # Business logic orchestration
│   │   ├── create_card.py
│   │   ├── process_ocr.py
│   │   ├── validate_card.py
│   │   └── list_cards.py
│   └── interfaces/            # Abstract interfaces (Ports)
│       ├── card_repository.py
│       ├── image_repository.py
│       ├── ocr_service.py
│       └── storage_service.py
│
├── infrastructure/            # 🔌 EXTERNAL SERVICES (Adapters)
│   ├── database/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   └── repositories/      # Repository implementations
│   ├── external/
│   │   ├── groq_ocr_service.py
│   │   └── local_storage.py
│   └── logging/
│       └── logger.py
│
├── api/                       # 🎯 PRESENTATION LAYER
│   ├── dependencies.py        # FastAPI dependencies
│   ├── cards.py               # Card endpoints
│   ├── images.py              # Image endpoints
│   └── ocr.py                 # OCR endpoints
│
├── schemas/                   # 📋 DTOs (Data Transfer Objects)
│   ├── card.py                # CardCreateDTO, CardResponseDTO
│   ├── image.py               # ImageUploadDTO, ImageResponseDTO
│   └── ocr.py                 # OCRRequestDTO, OCRResponseDTO
│
└── core/                      # ⚙️ CONFIGURATION
    ├── config.py              # Settings, environment variables
    └── database.py            # Database connection setup
```

## 🔄 Request Flow Example

### Creating a Card via API

```
1. API Layer (Presentation)
   ↓
   POST /api/cards with CardCreateDTO
   
2. Dependency Injection
   ↓
   - Inject ICardRepository
   - Inject Session
   
3. Use Case (Application)
   ↓
   CreateCardUseCase.execute()
   - Validate input
   - Create domain entity (Card)
   - Call repository.save()
   
4. Repository (Infrastructure)
   ↓
   SQLAlchemyCardRepository.save()
   - Convert entity → ORM model
   - Save to database
   - Convert ORM model → entity
   
5. Response
   ↓
   Convert entity → CardResponseDTO
   Return JSON to client
```

## 🧪 Testing Strategy

| Layer | Test Type | What to Test | Mock |
|-------|-----------|--------------|------|
| **Domain** | Unit | Entity validation, business rules | Nothing (pure) |
| **Application** | Unit | Use case logic | Repositories, Services |
| **Infrastructure** | Integration | Repository operations, API calls | Database (in-memory) |
| **API** | E2E | Full request → response | Nothing (real flow) |

## 🚀 Development Workflow

### Adding a New Feature

1. **Define domain entity** (`domain/entities/`)
2. **Create repository interface** (`application/interfaces/`)
3. **Implement use case** (`application/use_cases/`)
4. **Create DTOs** (`schemas/`)
5. **Implement repository** (`infrastructure/database/repositories/`)
6. **Create API endpoint** (`api/`)
7. **Setup dependency injection** (`api/dependencies.py`)
8. **Write tests** (unit → integration → e2e)

### Example: Add "Archive Card" Feature

```python
# 1. Domain entity (already exists, just add method)
class Card:
    def archive(self):
        self.status = "archived"

# 2. Repository interface
class ICardRepository:
    async def archive(self, card_id: int) -> bool:
        pass

# 3. Use case
class ArchiveCardUseCase:
    def __init__(self, repository: ICardRepository):
        self.repository = repository
    
    async def execute(self, card_id: int) -> Card:
        card = await self.repository.get_by_id(card_id)
        if not card:
            raise CardNotFoundError()
        card.archive()
        return await self.repository.update(card)

# 4. DTO
class CardArchiveResponseDTO(BaseModel):
    id: int
    status: str

# 5. Repository implementation
class SQLAlchemyCardRepository:
    async def archive(self, card_id: int) -> bool:
        # Implementation
        pass

# 6. API endpoint
@router.patch("/{card_id}/archive")
async def archive_card(card_id: int, repo=Depends(get_repo)):
    use_case = ArchiveCardUseCase(repo)
    card = await use_case.execute(card_id)
    return CardArchiveResponseDTO.from_entity(card)
```

## 📚 Key Concepts

### Entities vs DTOs
- **Entity**: Domain object with business logic (lives in memory)
- **DTO**: Data structure for transferring data (API input/output)
- **ORM Model**: Database representation (SQLAlchemy)

### Ports vs Adapters
- **Port**: Interface defined in application layer (e.g., `ICardRepository`)
- **Adapter**: Implementation in infrastructure layer (e.g., `SQLAlchemyCardRepository`)

### Use Cases vs Services
- **Use Case**: Single business operation (e.g., `CreateCard`)
- **Service**: Reusable utility (e.g., `OCRService`, `StorageService`)

## ✅ Best Practices Checklist

- [ ] Domain entities are pure Python (no FastAPI/SQLAlchemy imports)
- [ ] Use cases depend on interfaces, not implementations
- [ ] API endpoints only do validation + routing
- [ ] Business logic is in use cases or entities
- [ ] DTOs are used for API input/output
- [ ] Repository pattern for data access
- [ ] Dependency injection everywhere
- [ ] Custom exceptions for domain errors
- [ ] Comprehensive logging
- [ ] Type hints on all functions
- [ ] Tests for each layer

---

**Remember**: The inner layers (Domain, Application) should NEVER depend on outer layers (Infrastructure, Presentation).
