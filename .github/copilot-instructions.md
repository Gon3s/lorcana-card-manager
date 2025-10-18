# GitHub Copilot Instructions - Lorcana Card Manager

## 🎯 Project Overview

**Lorcana Card Manager**: Application web pour ajouter et visualiser des cartes Lorcana via OCR.

**Architecture**:
- 🐍 Backend: FastAPI (Python)
- 🎨 Frontend: Angular (TypeScript)
- 💾 Database: SQLite
- 🐳 Deployment: Docker (3 containers)

**Separation of concerns**:
- ✅ Ce projet: Gestion des cartes (ajout/visualisation)
- ✅ `lorcana_price`: Tracking des prix (Google Sheets + scrapers)

---

## 📁 Hierarchical Context

**This file contains GLOBAL instructions for the entire project.**

Specific instructions for each component are in:
- `backend/.github/copilot-instructions.md` → Python/FastAPI
- `frontend/.github/copilot-instructions.md` → Angular/TypeScript
- `database/.github/copilot-instructions.md` → SQL/Migrations

⚠️ **When working in a specific folder, follow its local instructions first.**

---

## 🏗️ Architecture & Components

### Backend API (FastAPI)
- RESTful API with OpenAPI documentation
- OCR service using Groq API
- Image upload and storage
- SQLAlchemy ORM with SQLite

### Frontend (Angular)
- Reactive UI with RxJS
- Image upload with drag & drop
- Card validation interface
- List and detail views with filters

### Database (SQLite)
- `cards`: Card information
- `card_images`: Image metadata and status
- `ocr_logs`: OCR processing history

---

## 🔄 Workflow

1. **Upload**: User uploads card image
2. **OCR**: Groq API extracts card information
3. **Validation**: User reviews and corrects data
4. **Storage**: Card saved with 'validated' status
5. **Visualization**: Browse and edit cards

### Image States
- `non_traite`: Uploaded, not processed
- `en_cours`: OCR in progress
- `attente_validation`: Awaiting user validation
- `valide`: Validated and saved

---

## 📐 Shared Data Models

### CardInfo (Pydantic)
Used for OCR extraction and validation:
- `encre`: Ink color (Amber, Amethyst, Emerald, Ruby, Sapphire, Steel)
- `encrable`: Whether card is inkable (boolean)
- `nom`: Card name
- `sous_titre`: Subtitle
- `mots_cles`: Keywords list
- `force`: Strength value
- `volonte`: Willpower value
- `texte`: Ability text
- `lore`: Lore value
- `rarete`: Rarity (Common, Uncommon, Rare, Super Rare, Legendary, Enchanted)
- `cout`: Ink cost

---

## 🎨 Code Conventions

### Architecture Principles
- **SOLID Principles**: Apply Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Architecture**: Separate Domain, Application, Infrastructure, and Presentation layers
- **Dependency Rule**: Dependencies point INWARD (outer layers depend on inner layers, never reverse)
- **Separation of Concerns**: Each module has a single, well-defined responsibility

### General
- Use descriptive variable names
- Add docstrings to all functions/classes
- Handle errors gracefully with custom exceptions
- Use logging instead of print statements
- Type hints everywhere (Python, TypeScript)
- Dependency Injection over direct instantiation
- Interfaces/Abstract classes for contracts

### Backend (Python/FastAPI)
- **Domain Layer**: Pure Python entities, no framework dependencies
- **Application Layer**: Use cases (business logic), repository interfaces
- **Infrastructure Layer**: Database, external services, file storage
- **Presentation Layer**: API endpoints, DTOs (Pydantic schemas)
- Repository Pattern for data access
- Use cases for business logic orchestration

### Frontend (Angular)
- **Smart/Dumb Components**: Smart (container) vs Dumb (presentational)
- **Services**: Business logic and API calls
- **RxJS**: Reactive state management
- **Dependency Injection**: Angular's DI system
- **Single Responsibility**: One component, one purpose

### Git Commits
- **Format**: `<gitmoji> <type>: <description>` (ONE LINE ONLY)
- Use gitmoji for commit type
- Keep commits focused and atomic

**Examples**:
```
✨ feat: add card upload endpoint
🐛 fix: handle OCR timeout errors
♻️ refactor: improve image storage service
📝 docs: update API documentation
```

### No Extra Documentation
- ❌ Don't create summary .md files after each task
- ❌ Don't create PHASE_COMPLETE.md files
- ❌ Don't create verbose commit message files
- ✅ Write code, test it, commit with one-line message
- ✅ Documentation only when it's needed (README, API docs)

---

## 🔗 Integration Points

### Between Components
- Backend exposes REST API at `/api/*`
- Frontend consumes API via HTTP services
- Docker volumes for SQLite persistence and image storage

### With lorcana_price project
- Shared data model concepts (CardInfo)
- Potential future integration for price tracking
- Common logging and error handling patterns

---

## 🐳 Docker Structure

Three services: backend (FastAPI), frontend (Angular), volumes for data persistence.

**Ports**:
- Backend: 8000
- Frontend: 4200

**Volumes**:
- SQLite database
- Uploaded images

---

## 📝 Important Notes

### Security
- Validate all file uploads (MIME type, size)
- Sanitize user inputs
- Use environment variables for secrets

### Performance
- Implement pagination for card lists
- Optimize database queries with indexes
- Handle large images efficiently

### Errors
- Return appropriate HTTP status codes
- Provide clear error messages
- Log errors with context for debugging

---

## 🚀 Quick Start

### Development
```bash
docker-compose up --build
```

### Access
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:4200
