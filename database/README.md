# 💾 Database - Lorcana Card Manager

## 📋 Vue d'ensemble

Cette documentation décrit le schéma de base de données SQLite.

**⚠️ Note importante** : Les fichiers de migration Alembic et le script de seed sont maintenant dans `backend/` car ils font partie intégrante de l'application FastAPI.

## � Structure

```
backend/
├── alembic/                      # Migrations Alembic
│   ├── env.py                    # Configuration Alembic
│   ├── script.py.mako            # Template pour migrations
│   └── versions/
│       └── 001_initial_schema.py # Migration initiale
├── alembic.ini                   # Configuration Alembic
├── seed.py                       # Script de seed avec données test
├── init_db.sh                    # Script d'initialisation
└── app/
    └── models/                   # Modèles SQLAlchemy
        ├── card.py
        ├── card_image.py
        └── ocr_log.py

database/
├── .github/
│   └── copilot-instructions.md  # Contexte IA pour SQL/Migrations
└── README.md                     # Ce fichier (documentation)
```

## 📊 Schéma de la base de données

### Table `cards`

Stocke les informations des cartes Lorcana.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique |
| `nom` | VARCHAR(255) | Nom de la carte |
| `sous_titre` | VARCHAR(255) | Sous-titre |
| `encre` | VARCHAR(50) | Couleur (Amber, Amethyst, Emerald, Ruby, Sapphire, Steel) |
| `encrable` | BOOLEAN | Carte encrable ou non |
| `cout` | INTEGER | Coût en encre |
| `force` | INTEGER | Force (personnages) |
| `volonte` | INTEGER | Volonté (personnages) |
| `lore` | INTEGER | Valeur de connaissance |
| `mots_cles` | TEXT | Mots-clés (JSON ou CSV) |
| `texte` | TEXT | Texte d'aptitude (langue originale) |
| `texte_fr` | TEXT | Texte d'aptitude (français) |
| `rarete` | VARCHAR(50) | Rareté (Common, Uncommon, Rare, Super Rare, Legendary, Enchanted) |
| `image_path` | VARCHAR(500) | Chemin vers l'image |
| `status` | VARCHAR(50) | État (`attente_validation`, `valide`) |
| `created_at` | DATETIME | Date de création |
| `updated_at` | DATETIME | Date de modification |

**Indexes:**
- `idx_card_search`: (nom, encre, rarete)
- `idx_card_status_created`: (status, created_at)

### Table `card_images`

Suivi des images uploadées et leur statut de traitement.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique |
| `card_id` | INTEGER (FK) | Référence vers `cards.id` (nullable) |
| `original_path` | VARCHAR(500) | Chemin de l'image uploadée |
| `status` | VARCHAR(50) | État (`non_traite`, `en_cours`, `attente_validation`, `valide`) |
| `created_at` | DATETIME | Date d'upload |

**Indexes:**
- `idx_image_status_created`: (status, created_at)

### Table `ocr_logs`

Historique des traitements OCR.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique |
| `card_image_id` | INTEGER (FK) | Référence vers `card_images.id` |
| `raw_response` | TEXT | Réponse brute de l'API Groq (JSON) |
| `error_message` | TEXT | Message d'erreur si échec |
| `created_at` | DATETIME | Date du traitement |

**Indexes:**
- `idx_ocr_image_created`: (card_image_id, created_at)

## 🔄 Workflow des états

### Images (`card_images.status`)

```
non_traite → en_cours → attente_validation → valide
```

1. **non_traite**: Image uploadée, pas encore traitée
2. **en_cours**: OCR en cours d'exécution
3. **attente_validation**: OCR terminé, données à valider
4. **valide**: Carte validée et sauvegardée

### Cartes (`cards.status`)

```
attente_validation → valide
```

1. **attente_validation**: Carte créée après OCR, à valider
2. **valide**: Carte validée par l'utilisateur

## 🚀 Utilisation

### Migrations Alembic

⚠️ **Toutes les commandes Alembic doivent être exécutées depuis le dossier `backend/`**

#### Appliquer les migrations

```bash
# Depuis le dossier backend/
cd backend

# Appliquer toutes les migrations
alembic upgrade head

# Ou utiliser le script d'initialisation
./init_db.sh
```

#### Créer une nouvelle migration

```bash
# Depuis le dossier backend/
cd backend

# Migration vide
alembic revision -m "description de la migration"

# Migration auto-générée (détecte les changements des modèles)
alembic revision --autogenerate -m "description"
```

#### Revenir en arrière

```bash
# Depuis le dossier backend/
cd backend

# Revenir d'une migration
alembic downgrade -1

# Revenir à une migration spécifique
alembic downgrade 001_initial_schema

# Tout supprimer
alembic downgrade base
```

#### Afficher l'historique

```bash
# Depuis le dossier backend/
cd backend

# Voir l'historique des migrations
alembic history

# Voir la migration actuelle
alembic current
```

### Script de seed

#### Insérer des données de test

```bash
# Depuis le dossier backend/
cd backend

# Seed simple
python seed.py

# Clear + seed
python seed.py --clear

# Clear uniquement
python seed.py --clear-only
```

Le script crée :
- 6 cartes d'exemple (différentes encres et raretés)
- 5 images avec différents statuts
- 3 logs OCR (succès et erreur)

## 🔧 Configuration

### Variables d'environnement

```bash
# URL de la base de données
DATABASE_URL=sqlite:///./lorcana_cards.db

# Depuis Docker
DATABASE_URL=sqlite:////app/data/lorcana_cards.db
```

### Fichiers de configuration

- **`alembic.ini`**: Configuration Alembic (logging, chemins)
- **`migrations/env.py`**: Script d'environnement pour migrations

## 📝 Bonnes pratiques

### Migrations

1. **Toujours tester** les migrations avant de les committer
2. **Nommer clairement** les migrations (ex: `add_card_type_field`)
3. **Inclure un downgrade** fonctionnel dans chaque migration
4. **Versionner** les migrations dans Git
5. **Ne jamais modifier** une migration déjà appliquée en production

### Seed

1. Utiliser des **données réalistes** pour tester les cas d'usage
2. Inclure des **edge cases** (valeurs nulles, statuts variés)
3. Rendre le script **idempotent** (clear avant seed)

### Performance

1. **Indexes** sur les colonnes fréquemment recherchées (nom, encre, status)
2. **Indexes composites** pour les requêtes multi-colonnes
3. **Foreign keys** pour l'intégrité référentielle
4. **Cascade delete** pour nettoyer les données orphelines

## 🔗 Intégration avec le backend

Les modèles SQLAlchemy sont définis dans `backend/app/models/` :

- `card.py`: Modèle Card
- `card_image.py`: Modèle CardImage
- `ocr_log.py`: Modèle OCRLog
- `base.py`: Base SQLAlchemy

Les migrations Alembic sont dans `backend/alembic/` et importent automatiquement ces modèles pour détecter les changements.

## 🐳 Utilisation avec Docker

Dans `docker-compose.yml`, la base SQLite est persistée via un volume :

```yaml
volumes:
  - ./data:/app/data
```

La base de données sera créée dans `./data/lorcana_cards.db`.

## 🆘 Troubleshooting

### Erreur "Target database is not up to date"

```bash
# Vérifier l'état actuel
alembic current

# Appliquer les migrations manquantes
alembic upgrade head
```

### Erreur "Can't locate revision identified by 'xxx'"

```bash
# Réinitialiser l'historique (attention: perte de données!)
alembic stamp head
```

### SQLite database locked

- Fermer toutes les connexions ouvertes
- Vérifier qu'aucun processus n'utilise la DB
- Redémarrer les containers Docker

## 📚 Ressources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 🎯 Prochaines étapes

- [ ] Ajouter des indexes full-text search (FTS5) pour recherche avancée
- [ ] Implémenter soft delete avec table `deleted_cards`
- [ ] Ajouter table `card_revisions` pour historique des modifications
- [ ] Considérer migration vers PostgreSQL si volume augmente
