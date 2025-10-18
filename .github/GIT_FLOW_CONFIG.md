# 🔧 Configuration Git Flow - Lorcana Card Manager

## 📊 État de la configuration (19 octobre 2025)

### Branches principales

#### 🔴 **main** (Production)
- **Rôle** : Branche de production stable
- **Protection** :
  - ✅ Nécessite 1 approbation pour merger
  - ✅ Historique linéaire obligatoire (`required_linear_history`)
  - ✅ Dismiss stale reviews activé
  - ❌ Force push interdit
  - ❌ Suppression interdite
  - ❌ Status checks requis : aucun (à configurer avec CI/CD)
- **Merge autorisé depuis** : `release/*`, `hotfix/*` uniquement
- **Branche par défaut** : Non

#### 🟢 **develop** (Développement)
- **Rôle** : Branche de travail principale pour le développement
- **Protection** :
  - ✅ **Aucune approbation requise** (permet auto-merge Dependabot)
  - ❌ Force push interdit
  - ❌ Suppression interdite
  - ❌ Status checks requis : aucun
- **Merge autorisé depuis** : `feature/*`, `bugfix/*`, PRs Dependabot
- **Branche par défaut** : **Oui** ✅

### Fonctionnalités activées

#### ✅ Auto-merge repository
```bash
gh repo edit --enable-auto-merge
```
Permet l'auto-merge des PRs quand toutes les conditions sont remplies.

#### ✅ Dependabot Auto-Merge
Workflow GitHub Actions (`.github/workflows/dependabot-auto-merge.yml`) :
- Active auto-merge pour patch et minor versions
- Approuve automatiquement les PRs avec security fixes
- Nécessite que tous les checks passent

### Branches temporaires

#### `feature/*`
- **Créées depuis** : `develop`
- **Mergées dans** : `develop`
- **Exemple** : `feature/phase-2.3-ocr-service`
- **Suppression** : Après merge (recommandé)

#### `bugfix/*`
- **Créées depuis** : `develop`
- **Mergées dans** : `develop`
- **Exemple** : `bugfix/upload-validation-error`
- **Suppression** : Après merge (recommandé)

#### `release/*`
- **Créées depuis** : `develop`
- **Mergées dans** : `main` ET `develop`
- **Exemple** : `release/v1.0.0`
- **Suppression** : Après double merge
- **Tag** : Version taggée sur `main`

#### `hotfix/*`
- **Créées depuis** : `main`
- **Mergées dans** : `main` ET `develop`
- **Exemple** : `hotfix/critical-security-fix`
- **Suppression** : Après double merge
- **Tag** : Version patch taggée sur `main`

## 🤖 Dependabot Configuration

### Mise à jour automatique
- **Fréquence** : Hebdomadaire (lundi 09:00)
- **Écosystèmes** : pip (backend), npm (frontend), GitHub Actions
- **Stratégie** :
  - **Patch/Minor** : Auto-merge si tests passent
  - **Major** : Review manuelle requise
  - **Security fixes** : Approbation automatique

### Fichiers de configuration
- `.github/dependabot.yml` : Configuration Dependabot
- `.github/workflows/dependabot-auto-merge.yml` : Workflow auto-merge
- `.github/DEPENDABOT.md` : Documentation complète

## 🎯 Stratégie de merge

### develop → main (via release)
```bash
# 1. Créer release depuis develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. Préparer la release
# - Bump version dans les fichiers de config
# - Mettre à jour CHANGELOG.md
# - Tester en environnement de staging
git commit -m "🔖 chore: prepare release v1.0.0"

# 3. Créer PR vers main
gh pr create --base main --head release/v1.0.0 --title "🔖 Release v1.0.0" --body "Release notes..."

# 4. Après approbation et merge
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# 5. Backmerge dans develop
git checkout develop
git merge --no-ff main
git push origin develop

# 6. Nettoyer
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### Hotfix urgent
```bash
# 1. Créer hotfix depuis main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Corriger le bug
git commit -m "🐛 fix: critical security vulnerability"

# 3. Créer PR vers main
gh pr create --base main --head hotfix/critical-bug --title "🐛 Hotfix: Critical bug" --body "Description..."

# 4. Après merge
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin main --tags

# 5. Backmerge dans develop
git checkout develop
git merge --no-ff main
git push origin develop

# 6. Nettoyer
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

## 📈 État actuel du projet

### Commits récents sur develop
```
5ad5342 build(deps)(deps): bump python-multipart (#4)
66778cd build(deps)(deps): bump httpx from 0.25.2 to 0.28.1 (#7)
b175f5a build(deps)(deps): bump python-dotenv from 1.0.0 to 1.1.1 (#6)
c55c4df build(deps)(deps): bump aiofiles from 24.1.0 to 25.1.0 (#3)
9e3e355 build(deps)(deps): bump pillow from 10.3.0 to 12.0.0 (#10)
8789418 build(deps)(deps): bump pytest from 7.4.3 to 8.4.2 (#8)
8e18c20 🤖 ci: configure Dependabot auto-merge
```

### Dépendances récentes mergées
- ✅ pytest 7.4.3 → 8.4.2
- ✅ Pillow 10.3.0 → 12.0.0 (MAJOR)
- ✅ aiofiles 24.1.0 → 25.1.0
- ✅ python-dotenv 1.0.0 → 1.1.1
- ✅ httpx 0.25.2 → 0.28.1
- ✅ python-multipart 0.0.18 → 0.0.20

### PRs Dependabot en cours
- ⏳ #12 : pydantic 2.5.0 → 2.12.3 (rebase en cours)
- ⏳ #11 : pydantic-settings 2.1.0 → 2.11.0 (rebase en cours)
- ⏳ #9 : alembic 1.12.1 → 1.17.0 (rebase en cours)
- ⏳ #5 : fastapi 0.104.1 → 0.119.0 (rebase en cours)

## 🔍 Vérification de la configuration

### Consulter les protections
```bash
# Protection main
gh api repos/Gon3s/lorcana-card-manager/branches/main/protection --jq '{required_approvals: .required_pull_request_reviews.required_approving_review_count, enforce_admins: .enforce_admins.enabled, required_status_checks: .required_status_checks.contexts}'

# Protection develop
gh api repos/Gon3s/lorcana-card-manager/branches/develop/protection --jq '{required_approvals: .required_pull_request_reviews.required_approving_review_count, enforce_admins: .enforce_admins.enabled, required_status_checks: .required_status_checks.contexts}'
```

### Vérifier auto-merge
```bash
gh repo view --json autoMergeAllowed --jq '.autoMergeAllowed'
```

## 📚 Références

- [GITFLOW.md](../GITFLOW.md) - Guide d'utilisation Git Flow
- [DEPENDABOT.md](DEPENDABOT.md) - Documentation Dependabot
- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

**Dernière mise à jour** : 19 octobre 2025  
**Maintenu par** : @Gon3s
