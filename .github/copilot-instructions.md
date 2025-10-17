# GitHub Copilot Instructions - Lorcana Card Manager# GitHub Copilot Instructions - Lorcana Card Manager



## 🎯 Project Overview## 🎯 Project Overview

**Lorcana Card Manager**: A web application for adding and visualizing new Lorcana cards via OCR.**Lorcana Card Manager**: A web application for adding and visualizing new Lorcana cards via OCR.



**Architecture**:**Architecture**:

- 🐍 Backend: FastAPI (Python)- 🐍 Backend: FastAPI (Python)

- 🎨 Frontend: Angular (TypeScript)- 🎨 Frontend: Angular (TypeScript)

- 💾 Database: SQLite- 💾 Database: SQLite

- 🐳 Deployment: Docker (3 containers)- 🐳 Deployment: Docker (3 containers)



**Separation of concerns**:**Separation of concerns**:

- ✅ This project: Card management (add/view)- ✅ This project: Card management (add/view)

- ✅ `lorcana_price`: Price tracking (Google Sheets + scrapers)- ✅ lorcana_price: Price tracking (Google Sheets + scrapers)



------



## 🏗️ Architecture & Components## 🏗️ Architecture & Components



### Backend API (FastAPI)### Backend API (FastAPI)

- RESTful API with automatic OpenAPI documentation- RESTful API with automatic OpenAPI documentation

- OCR service using Groq API- OCR service using Groq API

- Image upload and storage management- Image upload and storage management

- SQLAlchemy ORM with SQLite- SQLAlchemy ORM with SQLite



### Frontend (Angular)### Frontend (Angular)

- Reactive UI with RxJS- Reactive UI with RxJS

- Image upload with drag & drop- Image upload with drag & drop

- Card validation interface- Card validation interface

- List and detail views with filters- List and detail views with filters



### Database (SQLite)### Database (SQLite)

- `cards`: Card information- cards: Card information

- `card_images`: Image metadata and status- card_images: Image metadata and status

- `ocr_logs`: OCR processing history- ocr_logs: OCR processing history



------



## 🔄 Workflow## 🔄 Workflow



1. **Upload**: User uploads card image1. **Upload**: User uploads card image

2. **OCR**: Groq API extracts card information2. **OCR**: Groq API extracts card information

3. **Validation**: User reviews and corrects data3. **Validation**: User reviews and corrects data

4. **Storage**: Card saved with 'validated' status4. **Storage**: Card saved with 'validated' status

5. **Visualization**: Browse and edit cards5. **Visualization**: Browse and edit cards



### Image States### Image States

- `non_traite`: Uploaded, not processed- on_traite\: Uploaded, not processed

- `en_cours`: OCR in progress- \n_cours\: OCR in progress

- `attente_validation`: Awaiting user validation- \ttente_validation\: Awaiting user validation

- `valide`: Validated and saved- \alide\: Validated and saved



------



## 📐 Shared Data Models## 📐 Shared Data Models



### CardInfo (Pydantic)### CardInfo (Pydantic)

Used for OCR extraction and validation:

- encre: Ink color (Amber, Amethyst, Emerald, Ruby, Sapphire, Steel)

- encrable: Whether card is inkable (boolean)### Card States

- nom: Card name- on_traite\, \n_cours\, \ttente_validation\, \alide

- sous_titre: Subtitle---

- mots_cles: Keywords list

- force: Strength value## 🎨 Code Conventions

- volonte: Willpower value

- texte: Ability text### General

- lore: Lore value- Use descriptive variable names (English preferred)

- rarete: Rarity (Common, Uncommon, Rare, Super Rare, Legendary, Enchanted)- Add docstrings to all functions/classes

- cout: Ink cost- Handle errors gracefully with try/except

- Use logging instead of print statements

### Card States- Follow the principle of separation of concerns

- `non_traite`, `en_cours`, `attente_validation`, `valide`

### Git Commits

---- Use gitmoji for commit messages

- Follow conventional commits format

## 🎨 Code Conventions- Keep commits focused and atomic



### General**Examples**:

- Use descriptive variable names (English preferred)- ✨ \eat: add card upload endpoint- 🐛 \ix: handle OCR timeout errors- 📝 \docs: update API documentation- ♻️ \

- Add docstrings to all functions/classesefactor: improve image storage service

- Handle errors gracefully with try/except---

- Use logging instead of print statements

- Follow the principle of separation of concerns## 🔗 Integration Points



### Git Commits### Between Components

- Use gitmoji for commit messages- Backend exposes REST API at \/api/*- Frontend consumes API via HTTP services

- Follow conventional commits format- Docker volumes for SQLite persistence and image storage

- Keep commits focused and atomic

### With lorcana_price project

**Examples**:- Shared data model concepts (CardInfo)

- ✨ `feat: add card upload endpoint`- Potential future integration for price tracking

- 🐛 `fix: handle OCR timeout errors`- Common logging and error handling patterns

- 📝 `docs: update API documentation`

- ♻️ `refactor: improve image storage service`---



---## 🐳 Docker Structure



## 🔗 Integration Points



### Between Components---

- Backend exposes REST API at `/api/*`

- Frontend consumes API via HTTP services## 📝 Important Notes

- Docker volumes for SQLite persistence and image storage

### Security

### With lorcana_price project- Validate all file uploads (MIME type, size)

- Shared data model concepts (CardInfo)- Sanitize user inputs

- Potential future integration for price tracking- Use environment variables for secrets

- Common logging and error handling patterns

### Performance

---- Implement pagination for card lists

- Optimize database queries with indexes

## 🐳 Docker Structure- Handle large images efficiently



Three services: backend (FastAPI), frontend (Angular), volumes for data persistence.### Errors

- Return appropriate HTTP status codes

**Ports**:- Provide clear error messages

- Backend: 8000- Log errors with context for debugging

- Frontend: 4200

---

**Volumes**:

- SQLite database## 🚀 Quick Start

- Uploaded images

### Development

---



## 📝 Important Notes### Access

- Backend API: http://localhost:8000

### Security- API Docs: http://localhost:8000/docs

- Validate all file uploads (MIME type, size)- Frontend: http://localhost:4200

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
