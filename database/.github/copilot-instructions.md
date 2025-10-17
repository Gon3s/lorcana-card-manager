# GitHub Copilot Instructions - Database (SQLite)

## 💾 Database Structure

### Tables Overview
- `cards`: Main card information
- `card_images`: Image metadata and processing status
- `ocr_logs`: OCR processing history and raw responses

---

## 📋 Schema Definition

### cards Table
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    sous_titre VARCHAR(100),
    encre VARCHAR(20),
    cout INTEGER CHECK(cout >= 0 AND cout <= 20),
    encrable BOOLEAN DEFAULT FALSE,
    force INTEGER,
    volonte INTEGER,
    lore INTEGER,
    mots_cles TEXT,  -- JSON array stored as text
    texte TEXT,
    texte_fr TEXT,
    rarete VARCHAR(20),
    status VARCHAR(20) DEFAULT 'attente_validation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for common queries
    INDEX idx_cards_nom (nom),
    INDEX idx_cards_encre (encre),
    INDEX idx_cards_rarete (rarete),
    INDEX idx_cards_status (status),
    INDEX idx_cards_created_at (created_at)
);
```

### card_images Table
```sql
CREATE TABLE card_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER,
    original_path VARCHAR(255) NOT NULL,
    thumbnail_path VARCHAR(255),
    status VARCHAR(20) DEFAULT 'non_traite',
    file_size INTEGER,
    mime_type VARCHAR(50),
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
    
    INDEX idx_card_images_card_id (card_id),
    INDEX idx_card_images_status (status)
);
```

### ocr_logs Table
```sql
CREATE TABLE ocr_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_image_id INTEGER NOT NULL,
    raw_response TEXT,
    error_message TEXT,
    processing_time_ms INTEGER,
    api_model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (card_image_id) REFERENCES card_images(id) ON DELETE CASCADE,
    
    INDEX idx_ocr_logs_card_image_id (card_image_id),
    INDEX idx_ocr_logs_created_at (created_at)
);
```

---

## 🎯 Naming Conventions

### Tables
- Lowercase, plural: `cards`, `card_images`, `ocr_logs`
- Use underscores for multi-word names: `card_images`

### Columns
- Lowercase with underscores: `created_at`, `card_id`
- Primary keys: `id`
- Foreign keys: `{table}_id` (e.g., `card_id`)
- Timestamps: `created_at`, `updated_at`, `processed_at`
- Boolean flags: descriptive names (`encrable`, not `is_encrable`)

### Indexes
- Format: `idx_{table}_{column(s)}`
- Examples: `idx_cards_nom`, `idx_cards_encre_rarete`

---

## 🔑 Constraints and Relationships

### Primary Keys
- Always use `INTEGER PRIMARY KEY AUTOINCREMENT`
- Single column primary keys

### Foreign Keys
```sql
-- Enable foreign key constraints (important for SQLite)
PRAGMA foreign_keys = ON;

-- Standard foreign key pattern
FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
```

### Check Constraints
```sql
-- Validate ranges
cout INTEGER CHECK(cout >= 0 AND cout <= 20)

-- Validate enums
status VARCHAR(20) CHECK(status IN ('non_traite', 'en_cours', 'attente_validation', 'valide'))

-- Validate non-empty strings
nom VARCHAR(100) NOT NULL CHECK(LENGTH(nom) > 0)
```

---

## 🔍 Common Queries

### Pagination
```sql
SELECT * FROM cards
ORDER BY created_at DESC
LIMIT :limit OFFSET :offset;
```

### Search
```sql
-- Simple text search
SELECT * FROM cards
WHERE nom LIKE '%' || :query || '%'
   OR sous_titre LIKE '%' || :query || '%';

-- Full-text search (with FTS5 extension)
CREATE VIRTUAL TABLE cards_fts USING fts5(nom, sous_titre, texte, content=cards);

SELECT cards.* FROM cards
JOIN cards_fts ON cards.id = cards_fts.rowid
WHERE cards_fts MATCH :query;
```

### Filtering
```sql
-- Multiple filters
SELECT * FROM cards
WHERE 1=1
  AND (:encre IS NULL OR encre = :encre)
  AND (:rarete IS NULL OR rarete = :rarete)
  AND (:status IS NULL OR status = :status)
ORDER BY created_at DESC;
```

### Aggregations
```sql
-- Count by status
SELECT status, COUNT(*) as count
FROM cards
GROUP BY status;

-- Count by encre and rarete
SELECT encre, rarete, COUNT(*) as count
FROM cards
WHERE encre IS NOT NULL
GROUP BY encre, rarete
ORDER BY encre, rarete;
```

---

## 📊 Indexes Strategy

### When to Create Indexes
- Foreign keys (always)
- Columns used in WHERE clauses frequently
- Columns used in ORDER BY
- Columns used in JOIN conditions

### When NOT to Create Indexes
- Columns rarely queried
- Small tables (< 1000 rows)
- Columns with low cardinality (few distinct values)

### Composite Indexes
```sql
-- For queries filtering by multiple columns
CREATE INDEX idx_cards_encre_rarete ON cards(encre, rarete);

-- Good for:
SELECT * FROM cards WHERE encre = 'Amber' AND rarete = 'Rare';

-- Also good for:
SELECT * FROM cards WHERE encre = 'Amber';  -- Uses leftmost prefix

-- NOT good for:
SELECT * FROM cards WHERE rarete = 'Rare';  -- Doesn't use index
```

---

## 🔄 Migrations with Alembic

### Migration File Structure
```python
"""add cards table

Revision ID: 001
Revises: 
Create Date: 2025-10-17
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'cards',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nom', sa.String(100), nullable=False),
        sa.Column('sous_titre', sa.String(100)),
        sa.Column('encre', sa.String(20)),
        sa.Column('cout', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_cards_nom', 'cards', ['nom'])

def downgrade():
    op.drop_index('idx_cards_nom')
    op.drop_table('cards')
```

### Migration Best Practices
- One logical change per migration
- Always provide both `upgrade()` and `downgrade()`
- Test migrations on a copy of production data
- Keep migrations reversible when possible

---

## 🛠️ Maintenance Queries

### Vacuum (Reclaim Space)
```sql
-- Run periodically to optimize database
VACUUM;
```

### Analyze (Update Statistics)
```sql
-- Update query planner statistics
ANALYZE;
```

### Check Integrity
```sql
-- Verify database integrity
PRAGMA integrity_check;
```

### Database Info
```sql
-- Get database size
SELECT page_count * page_size as size 
FROM pragma_page_count(), pragma_page_size();

-- List all tables
SELECT name FROM sqlite_master 
WHERE type='table' 
ORDER BY name;

-- List all indexes
SELECT name, tbl_name FROM sqlite_master 
WHERE type='index' 
ORDER BY tbl_name, name;
```

---

## 📝 Data Types

### SQLite Type Affinity
SQLite uses type affinity (not strict types):
- `INTEGER`: Whole numbers
- `REAL`: Floating point
- `TEXT`: Strings
- `BLOB`: Binary data
- `NULL`: Null value

### Recommended Mappings
```python
# SQLAlchemy to SQLite
Integer -> INTEGER
String(n) -> TEXT
Text -> TEXT
Boolean -> INTEGER (0 or 1)
DateTime -> TEXT (ISO 8601 format)
Float -> REAL
```

---

## 🔒 Security

### SQL Injection Prevention
```python
# ❌ NEVER do this
query = f"SELECT * FROM cards WHERE nom = '{user_input}'"

# ✅ Always use parameterized queries
query = "SELECT * FROM cards WHERE nom = :nom"
result = db.execute(query, {"nom": user_input})
```

### Sensitive Data
- Don't store API keys in database
- Use environment variables for credentials
- Consider encryption for sensitive fields (if needed)

---

## 📊 Seed Data

### Example Seed Script
```sql
-- Insert sample cards for testing
INSERT INTO cards (nom, sous_titre, encre, cout, force, volonte, lore, rarete, status)
VALUES 
    ('Mickey Mouse', 'Brave Little Tailor', 'Steel', 5, 3, 4, 2, 'Rare', 'valide'),
    ('Elsa', 'Snow Queen', 'Sapphire', 8, NULL, NULL, 3, 'Legendary', 'valide'),
    ('Maleficent', 'Striking Fear', 'Amethyst', 6, 5, 5, 1, 'Super Rare', 'valide');
```

---

## 🚀 Performance Tips

### Query Optimization
- Use `EXPLAIN QUERY PLAN` to analyze queries
- Avoid `SELECT *`, specify columns needed
- Use `LIMIT` for large result sets
- Leverage indexes for WHERE, ORDER BY, JOIN

### Connection Pooling
```python
# Use connection pooling for concurrent access
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///./lorcana_cards.db',
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
```

### Write-Ahead Logging (WAL)
```sql
-- Enable WAL mode for better concurrency
PRAGMA journal_mode=WAL;
```

---

## 📚 Useful SQLite Commands

```sql
-- Show current database
.databases

-- Show table schema
.schema cards

-- Export to CSV
.mode csv
.output cards.csv
SELECT * FROM cards;
.output stdout

-- Import from CSV
.mode csv
.import cards.csv cards

-- Timing queries
.timer on
SELECT COUNT(*) FROM cards;
```
