# Protection des branches GitHub

## 🔒 Configuration à faire manuellement sur GitHub

Comme nous n'avons pas GitHub CLI, voici les étapes pour protéger les branches :

### 1. Protéger la branche `main`

1. Aller sur **GitHub.com** → Votre repo `lorcana-card-manager`
2. **Settings** → **Branches** (menu gauche)
3. Sous "Branch protection rules", cliquer **"Add rule"**
4. **Branch name pattern** : `main`
5. Cocher les options suivantes :
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (1 minimum)
   - ✅ **Require status checks to pass before merging** (si vous avez des CI/CD)
   - ✅ **Include administrators** (pour forcer les PR même pour vous)
   - ✅ **Restrict who can push to matching branches** (optionnel)
6. Cliquer **"Create"**

### 2. Protéger la branche `develop` (optionnel mais recommandé)

Répéter les mêmes étapes pour `develop` avec :
- **Branch name pattern** : `develop`
- ✅ **Require a pull request before merging**
- ⚠️ Ne pas cocher "Include administrators" sur develop (pour pouvoir merge les features directement)

### 3. Définir `develop` comme branche par défaut

1. **Settings** → **Branches**
2. Sous "Default branch", cliquer sur l'icône de switch
3. Sélectionner **`develop`**
4. Cliquer **"Update"** et confirmer

## 📋 Résultat attendu

- `main` : Branche de production, protégée, merge uniquement via PR depuis `develop`
- `develop` : Branche de développement, branche par défaut, reçoit les features
- `feature/*` : Branches de features, mergées dans `develop`
- `hotfix/*` : Branches de correctifs urgents, mergées dans `main` ET `develop`
- `release/*` : Branches de release, mergées dans `main` ET `develop`
