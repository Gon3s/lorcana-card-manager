# Testing Documentation - Lorcana Card Manager Backend

## 📋 Overview

Tests complets pour le backend avec pytest : tests unitaires, d'intégration et end-to-end.

## 🔧 Installation

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 📁 Structure des Tests

```
tests/
├── conftest.py              # Configuration et fixtures pytest
├── unit/                    # Tests unitaires (logique métier isolée)
│   └── test_upload_image_use_case.py
├── integration/             # Tests d'intégration (avec dépendances)
│   ├── test_image_repository.py
│   └── test_local_storage.py
└── e2e/                     # Tests end-to-end (API complète)
    ├── test_image_api.py
    └── test_health_api.py
```

## 🧪 Catégories de Tests

### Unit Tests (`@pytest.mark.unit`)
- **Objectif**: Tester la logique métier de manière isolée
- **Mocks**: Tous les services externes sont mockés
- **Vitesse**: Très rapide (< 1s)
- **Exemple**: `test_upload_image_use_case.py`

### Integration Tests (`@pytest.mark.integration`)
- **Objectif**: Tester l'interaction avec les dépendances réelles
- **Base de données**: SQLite en mémoire
- **File System**: Répertoires temporaires
- **Vitesse**: Rapide (< 5s)
- **Exemples**: Repository, Storage Service

### End-to-End Tests (`@pytest.mark.e2e`)
- **Objectif**: Tester l'API complète de bout en bout
- **Client**: TestClient FastAPI
- **Base de données**: SQLite de test
- **Vitesse**: Moyen (< 10s)
- **Exemples**: API endpoints

## 🚀 Lancer les Tests

### Tous les tests
```bash
pytest
```

### Par catégorie
```bash
# Tests unitaires uniquement
pytest -m unit

# Tests d'intégration uniquement
pytest -m integration

# Tests end-to-end uniquement
pytest -m e2e
```

### Par fichier
```bash
pytest tests/unit/test_upload_image_use_case.py
pytest tests/integration/test_image_repository.py
pytest tests/e2e/test_image_api.py
```

### Par test spécifique
```bash
pytest tests/unit/test_upload_image_use_case.py::TestUploadImageUseCase::test_execute_success_png
```

### Avec verbose
```bash
pytest -v
pytest -vv  # Extra verbose
```

### Avec couverture
```bash
# Couverture dans le terminal
pytest --cov=app --cov-report=term-missing

# Rapport HTML
pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

## 📊 Coverage Goals

- **Global**: > 80%
- **Domain Layer**: > 90% (logique métier critique)
- **Application Layer**: > 85% (use cases)
- **Infrastructure Layer**: > 70% (adapters)
- **API Layer**: > 80% (endpoints)

## 🔍 Fixtures Disponibles

### Database Fixtures
- `test_engine`: SQLAlchemy engine de test
- `test_db`: Session de base de données de test
- `client`: TestClient FastAPI avec override DB

### Storage Fixtures
- `temp_upload_dir`: Répertoire temporaire pour uploads

### Mock Fixtures (dans tests unitaires)
- `mock_repository`: Mock IImageRepository
- `mock_storage`: Mock IStorageService

## 📝 Conventions de Tests

### Naming
```python
class TestClassName:
    def test_method_name_expected_behavior(self):
        pass
```

### Structure AAA
```python
def test_something():
    # Arrange - Setup
    data = prepare_data()
    
    # Act - Execute
    result = function_to_test(data)
    
    # Assert - Verify
    assert result == expected
```

### Async Tests
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

## 🐛 Debugging

### Run with pdb
```bash
pytest --pdb  # Break on first failure
pytest -x --pdb  # Stop at first failure
```

### Print statements
```bash
pytest -s  # Show print outputs
```

### Specific test with verbose
```bash
pytest tests/unit/test_upload_image_use_case.py::TestUploadImageUseCase::test_execute_success_png -vv -s
```

## 🔄 CI/CD Integration

### GitHub Actions (example)
```yaml
- name: Run tests
  run: |
    cd backend
    source .venv/bin/activate
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./backend/coverage.xml
```

## 📚 Best Practices

1. **Fast Tests**: Unit tests doivent être ultra-rapides
2. **Isolation**: Chaque test doit être indépendant
3. **Clear Names**: Nom du test = documentation
4. **One Assertion**: Un test = un concept (mais plusieurs asserts OK)
5. **Mock External**: Mocker tout ce qui est externe (API, files, time)
6. **Clean Up**: Les fixtures s'occupent du nettoyage

## 🔗 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
