#!/bin/bash

# 🚀 Database initialization script
# This script initializes the database by running Alembic migrations

set -e  # Exit on error

echo "🗄️  Initializing Lorcana Card Manager Database..."

# Change to database directory
cd "$(dirname "$0")"

# Check if Alembic is installed
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic is not installed. Please install it first:"
    echo "   pip install alembic sqlalchemy"
    exit 1
fi

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head

echo "✅ Database initialized successfully!"
echo ""
echo "💡 To seed the database with test data, run:"
echo "   python seed.py"
echo ""
echo "💡 To clear and reseed the database, run:"
echo "   python seed.py --clear"
