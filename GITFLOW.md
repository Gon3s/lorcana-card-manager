# 🌊 Git Flow - Lorcana Card Manager

## 📋 Structure des branches

```
main (production)
  └── develop (développement)
       ├── feature/phase-2.3-ocr-service
       ├── feature/phase-3-frontend
       └── feature/phase-4-tests
```

## 🎯 Workflow Git Flow

### 1️⃣ **Démarrer une nouvelle feature**

```bash
# Depuis develop
git checkout develop
git pull origin develop

# Créer la branche feature
git checkout -b feature/phase-2.3-ocr-service
```

### 2️⃣ **Travailler sur la feature**

```bash
# Faire vos modifications
git add .
git commit -m "✨ feat: add OCR service with Groq API"

# Pousser la branche
git push -u origin feature/phase-2.3-ocr-service
```

### 3️⃣ **Finaliser la feature**

```bash
# Merger dans develop
git checkout develop
git pull origin develop
git merge --no-ff feature/phase-2.3-ocr-service
git push origin develop

# Supprimer la branche feature (optionnel)
git branch -d feature/phase-2.3-ocr-service
git push origin --delete feature/phase-2.3-ocr-service
```

### 4️⃣ **Créer une release**

```bash
# Créer branche release depuis develop
git checkout develop
git checkout -b release/v1.0.0

# Préparer la release (bump version, changelog, etc.)
git commit -m "🔖 chore: prepare release v1.0.0"

# Merger dans main
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# Merger dans develop aussi
git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# Supprimer la branche release
git branch -d release/v1.0.0
```

### 5️⃣ **Hotfix urgent**

```bash
# Créer branche hotfix depuis main
git checkout main
git checkout -b hotfix/critical-bug-fix

# Corriger le bug
git commit -m "🐛 fix: critical bug in upload service"

# Merger dans main
git checkout main
git merge --no-ff hotfix/critical-bug-fix
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin main --tags

# Merger dans develop aussi
git checkout develop
git merge --no-ff hotfix/critical-bug-fix
git push origin develop

# Supprimer la branche hotfix
git branch -d hotfix/critical-bug-fix
```

## 🎨 Conventions de nommage

### Branches
- `feature/*` : Nouvelles fonctionnalités (ex: `feature/phase-2.3-ocr-service`)
- `bugfix/*` : Corrections de bugs non urgents (ex: `bugfix/upload-validation`)
- `hotfix/*` : Corrections urgentes en production (ex: `hotfix/critical-security-issue`)
- `release/*` : Préparation de releases (ex: `release/v1.0.0`)
- `docs/*` : Documentation uniquement (ex: `docs/update-readme`)

### Commits (Conventional Commits)
- `✨ feat:` Nouvelle fonctionnalité
- `🐛 fix:` Correction de bug
- `📝 docs:` Documentation
- `♻️ refactor:` Refactoring sans changement fonctionnel
- `✅ test:` Ajout/modification de tests
- `🔧 chore:` Tâches diverses (deps, config)
- `🎨 style:` Formatage, style
- `⚡️ perf:` Amélioration de performance
- `🔒 security:` Correctif de sécurité

## 📊 État actuel du projet

```
✅ main : Production (Phase 1 + Phase 2.1 + Phase 2.2 complètes)
✅ develop : Développement (créée, identique à main pour l'instant)
```

## 🚀 Prochaines features

1. `feature/phase-2.3-ocr-service` - Service OCR avec Groq
2. `feature/phase-2.4-crud-cards` - CRUD des cartes
3. `feature/phase-3-frontend` - Interface Angular
4. `feature/phase-4-docker` - Finalisation Docker

## 📚 Ressources

- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
