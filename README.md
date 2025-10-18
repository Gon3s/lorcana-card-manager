# Lorcana Card Manager

Une application web pour ajouter et visualiser les cartes Lorcana via OCR.

## 🎯 Vue d'ensemble

**Lorcana Card Manager** permet de :
- 📤 Uploader des images de cartes
- 🤖 Extraire automatiquement les informations via OCR (Groq API)
- ✅ Valider et corriger les données extraites
- 📊 Visualiser et gérer la collection de cartes

## 🏗️ Architecture

```
lorcana-card-manager/
├── backend/          # FastAPI (Python)
├── frontend/         # Angular (TypeScript)
├── database/         # SQLite + Migrations
├── docker/           # Dockerfiles & compose
├── .github/          # Contextes IA Copilot
└── docs/             # Documentation
```

### Technologies
- 🐍 **Backend**: FastAPI, SQLAlchemy, Groq API
- 🎨 **Frontend**: Angular 17+, RxJS, TypeScript
- 💾 **Database**: SQLite
- 🐳 **Déploiement**: Docker Compose (3 containers)

## 🚀 Quick Start

### Prérequis
- Docker et Docker Compose installés sur WSL
- Clé API Groq

### Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd lorcana-card-manager
```

2. **Configuration**
```bash
cp .env.example .env
# Éditer .env et ajouter GROQ_API_KEY
```

3. **Lancer l'application**
```bash
docker-compose up --build
```

### Accès
- 🌐 Frontend: http://localhost:4200
- 🔌 API Backend: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 🔄 Workflow

1. **Upload** : L'utilisateur uploade une image de carte
2. **OCR** : L'API Groq extrait les informations de la carte
3. **Validation** : L'utilisateur vérifie et corrige si nécessaire
4. **Stockage** : La carte est sauvegardée avec le statut "validé"
5. **Visualisation** : Navigation et édition des cartes

### États des images
- `non_traite` : Image uploadée, non traitée
- `en_cours` : OCR en cours
- `attente_validation` : En attente de validation utilisateur
- `valide` : Validée et sauvegardée

## 📐 Structure de la base de données

### Tables principales

**cards** : Informations des cartes
- Nom, sous-titre, encre, coût, force, volonté, lore
- Mots-clés, texte d'habileté, rareté
- Timestamps (création, modification)

**card_images** : Métadonnées des images
- Chemin de l'image, statut, dimensions
- Relation avec la carte

**ocr_logs** : Historique des traitements OCR
- Réponse brute de l'API
- Messages d'erreur
- Temps de traitement

## 🛠️ Développement

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Angular)

```bash
cd frontend
npm install
npm start
```

### Database Migrations

```bash
cd backend
alembic upgrade head    # Appliquer les migrations
alembic revision -m "description"  # Créer une migration

# Ou utiliser le script d'initialisation
./init_db.sh

# Seed avec données de test
python seed.py --clear
```

## 📝 API Endpoints

### Images
- `POST /api/images/upload` - Upload une image
- `POST /api/ocr/process/{image_id}` - Traiter l'OCR

### Cards
- `GET /api/cards` - Liste des cartes (pagination, filtres)
- `GET /api/cards/{id}` - Détails d'une carte
- `PUT /api/cards/{id}` - Mettre à jour une carte
- `PATCH /api/cards/{id}/status` - Changer le statut
- `DELETE /api/cards/{id}` - Supprimer une carte

## 🧪 Tests

### Backend
```bash
cd backend
pytest
pytest --cov=app tests/  # Avec coverage
```

### Frontend
```bash
cd frontend
npm test                 # Unit tests
npm run e2e             # E2E tests
```

## 🐳 Docker

### Build et lancement
```bash
docker-compose up --build
```

### Arrêt
```bash
docker-compose down
```

### Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📦 Déploiement

### Sur serveur local (WSL)

```bash
# Sur le serveur
cd ~/Dev/lorcana-card-manager
git pull
docker-compose down
docker-compose up --build -d
```

### Backup de la base de données

```bash
# Backup
docker-compose exec backend cp /app/lorcana_cards.db /app/backups/backup_$(date +%Y%m%d_%H%M%S).db

# Restore
docker-compose exec backend cp /app/backups/backup_20251017_120000.db /app/lorcana_cards.db
docker-compose restart backend
```

## 🔗 Lien avec lorcana_price

Ce projet est **complémentaire** au projet `lorcana_price` :

- **lorcana_price** : Tracking des prix (Cardmarket, Vinted)
- **lorcana-card-manager** : Gestion des nouvelles cartes

Les deux projets partagent :
- Modèles de données similaires (`CardInfo`)
- Conventions de code (Pydantic, logging)
- Patterns d'architecture

## 🤖 Contextes IA Copilot

Le projet utilise des **contextes IA hiérarchisés** :

- `.github/copilot-instructions.md` : Contexte global (architecture, workflow)
- `backend/.github/copilot-instructions.md` : Spécifique Python/FastAPI
- `frontend/.github/copilot-instructions.md` : Spécifique Angular/TypeScript
- `database/.github/copilot-instructions.md` : Spécifique SQL/Migrations

Ces contextes guident GitHub Copilot pour générer du code cohérent.

## 🌊 Git Flow

Ce projet utilise **Git Flow** pour la gestion des branches :

- `main` : Production (protégée, merge via PR uniquement)
- `develop` : Développement (branche par défaut)
- `feature/*` : Nouvelles fonctionnalités
- `hotfix/*` : Correctifs urgents

**Démarrer une nouvelle feature :**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nom-de-la-feature
# ... travail ...
git push -u origin feature/nom-de-la-feature
# Créer PR vers develop sur GitHub
```

📖 Voir [GITFLOW.md](GITFLOW.md) pour le workflow complet.

## 📚 Documentation

- [Roadmap du projet](ROADMAP.md)
- [Workflow Git Flow](GITFLOW.md)
- [Architecture Clean Architecture](backend/ARCHITECTURE.md)
- [Tests (pytest + Bruno)](backend/tests/README.md)
- [Protection des branches](.github/workflows/protect-branches.md)

## 🐛 Troubleshooting

### Erreur de connexion à l'API
- Vérifier que `GROQ_API_KEY` est configurée dans `.env`
- Vérifier les logs backend : `docker-compose logs backend`

### Erreur de base de données
- Réinitialiser : `docker-compose down -v && docker-compose up --build`

### Problème de permissions WSL
```bash
sudo chown -R $USER:$USER ~/Dev/lorcana-card-manager
```

## 📄 License

À définir

## 👤 Auteur

Gon3s

## 🙏 Remerciements

- Groq API pour l'OCR
- Projet `lorcana_price` pour les fondations
