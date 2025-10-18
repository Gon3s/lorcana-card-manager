# 🗺️ Roadmap - Lorcana Card Manager

## 📋 Vue d'ensemble du projet

**Objectif** : Créer une application web pour ajouter et visualiser les nouvelles cartes Lorcana via OCR.

**Architecture** :
- 🐍 **Backend API** : FastAPI (Python)
- 💾 **Base de données** : SQLite
- 🎨 **Frontend** : Angular
- 🐳 **Containerisation** : Docker (3 services)
- 📦 **Déploiement** : Git push/pull sur serveur local

**Séparation des responsabilités** :
- ✅ **Nouveau projet** : Gestion des cartes (ajout/visualisation)
- ✅ **Projet actuel** : Tracking des prix (Google Sheets + scrapers)

---

## 🎯 Phase 1 : Fondations & Infrastructure

### 1.1 Structure du projet
- [x] **Créer le dossier sur WSL** (accès à Docker)
  ```bash
  # Sur WSL
  cd ~
  mkdir -p Dev/lorcana-card-manager
  cd Dev/lorcana-card-manager
  ```
- [x] Créer la structure de dossiers (mono-repo)
  ```
  lorcana-card-manager/
  ├── backend/          # FastAPI
  │   └── .github/      # Contexte IA Python/FastAPI
  ├── frontend/         # Angular
  │   └── .github/      # Contexte IA Angular/TypeScript
  ├── database/         # Scripts SQL & migrations
  │   └── .github/      # Contexte IA SQL
  ├── docker/           # Dockerfiles & docker-compose
  ├── .github/          # CI/CD & copilot-instructions GLOBAL
  └── docs/             # Documentation
  ```
- [x] Configurer les contextes IA hiérarchisés
  - [x] `.github/copilot-instructions.md` (GLOBAL - tous les composants)
  - [x] `backend/.github/copilot-instructions.md` (Python/FastAPI)
  - [x] `frontend/.github/copilot-instructions.md` (Angular/TypeScript)
  - [x] `database/.github/copilot-instructions.md` (SQL/Migrations)
- [x] Initialiser Git avec `.gitignore` adapté
- [x] Créer `README.md` principal avec architecture et commandes

### 1.2 Base de données SQLite ✅
- [x] Définir le schéma de données
  - Table `cards` (id, nom, sous_titre, encre, cout, force, volonte, lore, mots_cles, texte, texte_fr, rarete, image_path, status, created_at, updated_at)
  - Table `card_images` (id, card_id, original_path, status: non_traite|en_cours|attente_validation|valide, created_at)
  - Table `ocr_logs` (id, card_image_id, raw_response, error_message, created_at)
- [x] Créer les scripts de migration (Alembic)
- [x] Ajouter des indexes pour les recherches fréquentes
- [x] Script de seed pour données de test

### 1.3 Docker & Environnement ✅
- [x] **Vérifier Docker sur WSL** (non installé - fichiers créés pour installation future)
- [x] Créer `Dockerfile` pour le backend
- [x] Créer `Dockerfile` pour le frontend  
- [x] Créer `docker-compose.yml` (2 services : backend, frontend, volumes)
- [x] Configurer les volumes pour :
  - Persistance SQLite
  - Stockage des images uploadées
- [x] `.env.example` déjà créé en Phase 1.2
- [x] Documentation Docker complète dans `docker/README.md`

---

## 🚀 Phase 2 : Backend API (FastAPI)

### 2.1 Setup du projet FastAPI
- [ ] Initialiser FastAPI avec structure modulaire
  ```
  backend/
  ├── app/
  │   ├── api/          # Endpoints
  │   ├── core/         # Config, security
  │   ├── models/       # SQLAlchemy models
  │   ├── schemas/      # Pydantic schemas
  │   ├── services/     # Business logic
  │   └── utils/        # Helpers (OCR, logger)
  ├── tests/
  └── requirements.txt
  ```
- [ ] Configurer SQLAlchemy + SQLite
- [ ] Setup logger (réutiliser `utils/logger.py` du projet actuel)
- [ ] Configurer CORS pour Angular
- [ ] Ajouter health check endpoint (`/health`)

### 2.2 Gestion des images & Upload
- [ ] **POST** `/api/images/upload`
  - Recevoir l'image (multipart/form-data)
  - Valider le format (PNG, JPG)
  - Sauvegarder en local avec nom unique
  - Créer entrée `card_images` avec status `non_traite`
  - Retourner l'ID de l'image
- [ ] Service de stockage local des images
  - Dossier organisé par date : `uploads/YYYY-MM-DD/`
  - Génération de thumbnails (optionnel pour MVP)

### 2.3 Service OCR
- [ ] Créer service OCR (réutiliser code de `fill_sheet_with_ocr.py`)
  - Adapter pour Groq API
  - Utiliser le même prompt optimisé
  - Gérer les erreurs et timeouts
- [ ] **POST** `/api/ocr/process/{image_id}`
  - Mettre status à `en_cours`
  - Exécuter l'OCR
  - Logger le résultat brut dans `ocr_logs`
  - Créer entrée `cards` avec status `attente_validation`
  - Mettre status image à `attente_validation`
  - Retourner les données extraites
- [ ] Gestion des états asynchrone (optionnel : Celery/RQ pour queue)

### 2.4 CRUD Cartes
- [ ] **GET** `/api/cards`
  - Liste paginée des cartes
  - Filtres : status, encre, rarete, recherche texte
  - Tri : date, nom, rarete
- [ ] **GET** `/api/cards/{id}`
  - Détails complets d'une carte
  - Inclure l'image associée
- [ ] **PUT** `/api/cards/{id}`
  - Éditer tous les champs
  - Validation des données (Pydantic)
  - Mettre à jour `updated_at`
- [ ] **PATCH** `/api/cards/{id}/status`
  - Changer le status (attente_validation → valide)
- [ ] **DELETE** `/api/cards/{id}` (soft delete ou hard delete ?)

### 2.5 API Documentation
- [ ] Swagger UI automatique (`/docs`)
- [ ] Ajouter descriptions et exemples aux endpoints
- [ ] Exporter OpenAPI spec pour le frontend

---

## 🎨 Phase 3 : Frontend Angular

### 3.1 Setup du projet Angular
- [ ] Créer projet Angular (dernière version stable)
- [ ] Configurer routing
- [ ] Setup TailwindCSS ou Angular Material (UI framework)
- [ ] Configurer environnements (dev/prod)
- [ ] Service HTTP interceptor pour l'API

### 3.2 Module Upload & OCR
- [ ] **Page Upload** (`/upload`)
  - Composant drag & drop pour upload image
  - Affichage preview de l'image
  - Bouton "Lancer l'OCR"
  - Loader pendant le traitement
- [ ] **Service Upload**
  - Appel API `/api/images/upload`
  - Appel API `/api/ocr/process/{id}`
  - Gestion des erreurs (toasts/notifications)
- [ ] **Page Validation** (`/validate/{id}`)
  - Affichage de l'image originale
  - Formulaire pré-rempli avec données OCR
  - Tous les champs éditables
  - Bouton "Valider" → change status à `valide`
  - Bouton "Annuler" → retour à la liste

### 3.3 Module Visualisation
- [ ] **Page Liste** (`/cards`)
  - Table/Grid des cartes avec pagination
  - Filtres : encre, rareté, status
  - Barre de recherche (nom, mots-clés)
  - Tri par colonne
  - Actions : Voir détails, Éditer, Supprimer
- [ ] **Page Détails** (`/cards/{id}`)
  - Affichage complet des infos carte
  - Image en grand
  - Historique OCR (logs)
  - Bouton "Éditer"
- [ ] **Page Édition** (`/cards/{id}/edit`)
  - Formulaire complet
  - Validation côté client
  - Sauvegarde et retour aux détails

### 3.4 Composants partagés
- [ ] Composant `CardPreview` (vignette carte)
- [ ] Composant `CardForm` (formulaire réutilisable)
- [ ] Composant `StatusBadge` (badge coloré par status)
- [ ] Composant `ImageViewer` (zoom, lightbox)
- [ ] Service `CardService` (appels API)
- [ ] Service `NotificationService` (toasts)

---

## 🔗 Phase 4 : Intégration & Tests

### 4.1 Tests Backend
- [ ] Tests unitaires des services OCR
- [ ] Tests d'intégration des endpoints
- [ ] Tests de validation Pydantic
- [ ] Coverage minimum 70%

### 4.2 Tests Frontend
- [ ] Tests unitaires des composants clés
- [ ] Tests E2E avec Cypress/Playwright (parcours upload → validation → visualisation)

### 4.3 Intégration complète
- [ ] Tester le flux complet dans Docker
- [ ] Vérifier la persistance des données (volumes)
- [ ] Tester les erreurs et edge cases

---

## 📦 Phase 5 : Déploiement & Documentation

### 5.1 Préparation déploiement
- [ ] Créer script de déploiement (`deploy.sh`) pour WSL
  - Git pull
  - Docker compose down
  - Docker compose build
  - Docker compose up -d
- [ ] Configurer les secrets (`.env` sur serveur)
- [ ] Backup automatique SQLite (cron job sur WSL)

### 5.2 Documentation
- [ ] **README.md** : Installation locale et déploiement
- [ ] **API.md** : Documentation des endpoints
- [ ] **ARCHITECTURE.md** : Schéma des flux et composants
- [ ] **CONTRIBUTING.md** : Guidelines pour contribuer
- [ ] **CHANGELOG.md** : Suivi des versions

### 5.3 Déploiement initial
- [ ] Tester sur serveur local (WSL)
- [ ] Vérifier les logs (backend, nginx si proxy)
- [ ] Tester l'accès depuis Windows (localhost)
- [ ] Tester l'accès depuis le réseau local
- [ ] Backup initial de la base

---

## 🚀 Phase 6 : Améliorations futures (Post-MVP)

### 6.1 Features avancées
- [ ] **Batch upload** : Upload multiple d'images
- [ ] **Queue OCR** : Traitement asynchrone avec Celery/Redis
- [ ] **Export** : CSV, JSON des cartes
- [ ] **Import** : Depuis Google Sheets (migration)
- [ ] **Recherche avancée** : Full-text search avec SQLite FTS5
- [ ] **Statistiques** : Dashboard avec charts (répartition par encre, rareté, etc.)

### 6.2 UX & UI
- [ ] Dark mode
- [ ] Responsive mobile
- [ ] Raccourcis clavier
- [ ] Undo/Redo pour l'édition
- [ ] Prévisualisation temps réel pendant OCR

### 6.3 Infrastructure
- [ ] CI/CD avec GitHub Actions (tests + build)
- [ ] Monitoring (logs centralisés, métriques)
- [ ] Authentification (JWT, multi-utilisateurs)
- [ ] Rate limiting sur API
- [ ] HTTPS avec Let's Encrypt

### 6.4 Base de données
- [ ] Migration vers PostgreSQL (si volume augmente)
- [ ] Système de révisions (historique des modifications)
- [ ] Soft delete avec corbeille

---

## 📊 Priorisation des phases

| Phase | Priorité | Durée estimée | Dépendances |
|-------|----------|---------------|-------------|
| Phase 1 | 🔴 Critique | 1 session | - |
| Phase 2 | 🔴 Critique | 2-3 sessions | Phase 1 |
| Phase 3 | 🔴 Critique | 2-3 sessions | Phase 2 |
| Phase 4 | 🟡 Important | 1-2 sessions | Phases 2 & 3 |
| Phase 5 | 🟡 Important | 1 session | Phases 1-4 |
| Phase 6 | 🟢 Nice to have | À définir | Post-MVP |

---

## 🎯 Checklist MVP (Minimum Viable Product)

**Critères de succès** :
- ✅ Uploader une image de carte
- ✅ OCR automatique avec Groq
- ✅ Valider/corriger les données extraites
- ✅ Sauvegarder la carte en base SQLite
- ✅ Voir la liste des cartes validées
- ✅ Éditer une carte existante
- ✅ Déployable sur serveur local avec Docker

---

## 🔄 Lien avec le projet actuel

**Projet actuel (`lorcana_price`)** :
- Reste responsable du **tracking de prix** (Cardmarket, Vinted)
- Continue d'utiliser **Google Sheets** comme source
- Les scrapers et notificateurs restent inchangés
- Reste sur Windows (`C:\Users\gones\Dev\lorcana_price`)

**Nouveau projet (`lorcana-card-manager`)** :
- Gère uniquement les **nouvelles cartes**
- Base de données **SQLite séparée**
- **Hébergé sur WSL** (`~/Dev/lorcana-card-manager`) pour Docker
- Peut potentiellement consommer l'API de prix (future intégration)

**Contexte IA hiérarchisé** :
- `.github/copilot-instructions.md` **GLOBAL** (architecture, workflow, modèles partagés)
- `backend/.github/copilot-instructions.md` (Python/FastAPI)
- `frontend/.github/copilot-instructions.md` (Angular/TypeScript)
- `database/.github/copilot-instructions.md` (SQL/Migrations)
- Conventions de code communes (Pydantic, logging, structure)
- Modèles de données compatibles (`CardInfo` réutilisable)

---

## 📝 Notes importantes

### Réutilisation du code existant
- ✅ **OCR Logic** : `fill_sheet_with_ocr.py` → Service backend
- ✅ **Logger** : `utils/logger.py` → Backend utils
- ✅ **Modèles** : `models/card.py` → Adapter pour SQLAlchemy
- ✅ **Pydantic schemas** : Réutiliser `CardInfo` de `fill_sheet_with_ocr.py`

### Points d'attention
- ⚠️ **WSL & Docker** : Tout le projet doit être sur WSL pour utiliser Docker
- ⚠️ **Accès WSL** : Configurer l'accès aux ports depuis Windows
- ⚠️ **Stockage images** : Prévoir un système de nettoyage (images orphelines)
- ⚠️ **Rate limiting Groq** : Gérer les limites API (max requêtes/minute)
- ⚠️ **Sécurité** : Valider les uploads (types MIME, taille max)
- ⚠️ **Performances** : Pagination obligatoire sur la liste des cartes

### Variables d'environnement (.env)
```env
# Backend
GROQ_API_KEY=xxx
DATABASE_URL=sqlite:///./lorcana_cards.db
UPLOAD_FOLDER=/app/uploads
MAX_UPLOAD_SIZE=10485760  # 10MB

# Frontend (Angular environment)
API_BASE_URL=http://localhost:8000/api

# Docker
BACKEND_PORT=8000
FRONTEND_PORT=4200
```

---

## 🤝 Prochaines étapes

1. ✅ **Roadmap validée**
2. 🚀 **Phase 1.1** : Créer le projet sur WSL
   - Créer le dossier `~/Dev/lorcana-card-manager` sur WSL
   - Initialiser Git
   - Créer la structure de dossiers
   - Configurer les 4 contextes IA (Global + Backend + Frontend + Database)
3. **Phase 1.2** : Définir le schéma SQLite
4. **Phase 1.3** : Configurer Docker

**C'est parti ! 🚀**
