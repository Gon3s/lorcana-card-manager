# 🤖 Configuration Dependabot

Ce projet utilise **Dependabot** pour maintenir les dépendances à jour automatiquement.

## 📋 Configuration

### Auto-merge activé pour :

✅ **Patches de sécurité** (`version-update:semver-patch`)
- Exemple : `1.0.0` → `1.0.1`
- Merge automatique après validation des tests

✅ **Mises à jour mineures** (`version-update:semver-minor`)  
- Exemple : `1.0.0` → `1.1.0`
- Merge automatique si pas de breaking changes

❌ **Mises à jour majeures** (`version-update:semver-major`)
- Exemple : `1.0.0` → `2.0.0`
- Review manuelle requise (breaking changes possibles)

### Planification

| Écosystème | Fréquence | Jour | Heure | Limite PRs |
|------------|-----------|------|-------|------------|
| **Python (pip)** | Hebdomadaire | Lundi | 09:00 | 10 |
| **npm** | Hebdomadaire | Lundi | 09:00 | 10 |
| **GitHub Actions** | Mensuelle | - | - | 5 |

## 🔧 Workflow Auto-Merge

Le workflow `.github/workflows/dependabot-auto-merge.yml` :

1. **Détecte** les PRs Dependabot
2. **Analyse** le type de mise à jour (patch/minor/major)
3. **Approuve** automatiquement les patches de sécurité
4. **Active auto-merge** pour patch et minor (avec tests)
5. **Merge automatiquement** une fois les tests passés

## 📊 Conditions d'auto-merge

```yaml
Auto-merge SI :
  - Actor = dependabot[bot]
  ET
  - (update-type = patch OU update-type = minor)
  ET
  - Tests CI passent ✅
```

## 🚨 Alertes de sécurité

Les **CVE et alertes de sécurité** déclenchent des PRs **prioritaires** :
- Label automatique : `security`
- Approbation automatique
- Notification immédiate

## 🛠️ Commandes manuelles

Si tu veux contrôler Dependabot manuellement dans une PR :

```bash
# Forcer rebase
@dependabot rebase

# Recréer la PR
@dependabot recreate

# Merger manuellement
@dependabot merge

# Squash and merge
@dependabot squash and merge

# Ignorer cette version
@dependabot ignore this minor version
```

## 📝 Logs et monitoring

### Vérifier les PRs Dependabot

```bash
gh pr list --label dependencies
```

### Voir les alertes de sécurité

```bash
gh api repos/:owner/:repo/dependabot/alerts
```

### Statut des mises à jour

GitHub → **Insights** → **Dependency graph** → **Dependabot**

## ⚙️ Configuration locale

Pour tester la config Dependabot localement :

```bash
# Installer dependabot-cli
gem install dependabot-cli

# Tester la config
dependabot update -f .github/dependabot.yml
```

## 🔗 Ressources

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Auto-merge PRs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)

## 🎯 Best Practices

1. ✅ **Toujours avoir des tests** avant d'activer auto-merge
2. ✅ **Monitorer les alertes** de sécurité régulièrement
3. ✅ **Review manuellement** les mises à jour majeures
4. ✅ **Maintenir les tests à jour** pour détecter les breaking changes
5. ✅ **Vérifier les changelogs** des dépendances critiques

---

**Note** : L'auto-merge ne fonctionne que si :
- Les tests CI sont configurés et passent ✅
- La branche n'a pas de conflit 🔄
- Les règles de protection de branche autorisent le merge 🔒
