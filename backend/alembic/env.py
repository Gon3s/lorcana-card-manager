"""Alembic environment configuration for backend."""

import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add app directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Base and all models
from app.models.base import Base
from app.models.card import Card
from app.models.card_image import CardImage
from app.models.ocr_log import OCRLog

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lorcana_cards.db")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Override sqlalchemy.url in alembic config
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
