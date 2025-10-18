"""Add processed_at and error_message to card_images

Revision ID: e1314ecaadaa
Revises: 001_initial_schema
Create Date: 2025-10-18 22:58:27.611608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1314ecaadaa'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add processed_at column
    op.add_column('card_images', sa.Column('processed_at', sa.DateTime(), nullable=True))
    
    # Add error_message column
    op.add_column('card_images', sa.Column('error_message', sa.String(length=500), nullable=True))


def downgrade() -> None:
    # Remove columns
    op.drop_column('card_images', 'error_message')
    op.drop_column('card_images', 'processed_at')
