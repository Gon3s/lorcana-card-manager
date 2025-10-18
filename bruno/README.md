# Bruno API Tests - Lorcana Card Manager

## 📋 Overview

Collection de tests API pour le backend Lorcana Card Manager utilisant [Bruno](https://www.usebruno.com/).

## 🚀 Installation

```bash
# Via npm
npm install -g @usebruno/cli

# Ou télécharger Bruno Desktop
# https://www.usebruno.com/downloads
```

## 📁 Structure

```
bruno/
├── bruno.json              # Configuration de la collection
├── environments/           # Variables d'environnement
│   ├── local.bru          # Dev local (localhost:8000)
│   └── production.bru     # Prod (à configurer)
├── Health/                # Tests de santé
│   ├── Health Check.bru
│   └── Root Endpoint.bru
├── Images/                # Tests d'upload/récupération
│   ├── Upload Image.bru
│   ├── Get Image by ID.bru
│   ├── Upload Invalid Format.bru
│   └── Get Non-Existent Image.bru
└── test-data/            # Fichiers de test
    ├── test_card.png     # Carte valide pour tests
    └── invalid.txt       # Fichier invalide pour tests d'erreur
```

## 🧪 Utilisation

### Via Bruno Desktop

1. Ouvrir Bruno
2. File → Open Collection
3. Sélectionner le dossier `bruno/`
4. Choisir l'environnement "local"
5. Lancer les requêtes individuellement ou toute la collection

### Via CLI

```bash
# S'assurer que le backend tourne
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

# Dans un autre terminal, lancer les tests
cd /home/gones/Dev/lorcana-card-manager
bru run --env local bruno/

# Lancer un dossier spécifique
bru run --env local bruno/Health/

# Lancer un test spécifique
bru run --env local bruno/Images/Upload\ Image.bru
```

## 🎯 Tests Disponibles

### Health (Santé du service)
- ✅ **Health Check**: Vérifie que l'API répond
- ✅ **Root Endpoint**: Vérifie l'endpoint racine

### Images (Gestion d'images)
- ✅ **Upload Image**: Upload d'une image valide
- ✅ **Get Image by ID**: Récupération d'une image
- ✅ **Upload Invalid Format**: Test d'erreur (format invalide)
- ✅ **Get Non-Existent Image**: Test d'erreur (ID inexistant)

## 📊 Assertions

Chaque test vérifie :
- **Status codes**: 200, 201, 400, 404
- **Response structure**: Présence des champs requis
- **Data types**: Validation des types de données
- **Business logic**: Statuts, IDs, messages d'erreur

## 🔧 Variables

### Collection Variables
- `baseUrl`: URL de base de l'API
- `apiPrefix`: Préfixe des routes API (`/api`)
- `lastImageId`: ID de la dernière image uploadée (automatique)

### Environnements

**local** (par défaut):
- `baseUrl`: http://localhost:8000
- `apiPrefix`: /api

**production**:
- `baseUrl`: https://api.lorcana.example.com
- `apiPrefix`: /api

## 📝 Préparer les fichiers de test

```bash
# Créer le dossier test-data si nécessaire
mkdir -p bruno/test-data

# Copier une image de carte pour les tests
cp backend/uploads/2025-10-18/*.png bruno/test-data/test_card.png

# Créer un fichier invalide
echo "invalid content" > bruno/test-data/invalid.txt
```

## 🔄 Workflow

1. **Upload Image** → génère `lastImageId`
2. **Get Image by ID** → utilise `lastImageId`
3. Tests d'erreur indépendants

## 🐛 Debugging

```bash
# Verbose mode
bru run --env local --verbose bruno/

# Reporter JSON pour CI/CD
bru run --env local --reporter json bruno/ > test-results.json
```

## 📚 Documentation

- [Bruno CLI](https://docs.usebruno.com/cli/overview)
- [Bruno Scripting](https://docs.usebruno.com/scripting/introduction)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
