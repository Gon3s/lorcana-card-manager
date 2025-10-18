"""Initial database schema - Create cards, card_images, and ocr_logs tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-10-17 00:00:00

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the initial database schema."""
    
    # Create cards table
    op.create_table(
        'cards',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nom', sa.String(length=255), nullable=False),
        sa.Column('sous_titre', sa.String(length=255), nullable=True),
        sa.Column('encre', sa.String(length=50), nullable=False),
        sa.Column('encrable', sa.Boolean(), nullable=False, default=False),
        sa.Column('cout', sa.Integer(), nullable=True),
        sa.Column('force', sa.Integer(), nullable=True),
        sa.Column('volonte', sa.Integer(), nullable=True),
        sa.Column('lore', sa.Integer(), nullable=True),
        sa.Column('mots_cles', sa.Text(), nullable=True),
        sa.Column('texte', sa.Text(), nullable=True),
        sa.Column('texte_fr', sa.Text(), nullable=True),
        sa.Column('rarete', sa.String(length=50), nullable=False),
        sa.Column('image_path', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, default='attente_validation'),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for cards table
    op.create_index('ix_cards_id', 'cards', ['id'])
    op.create_index('ix_cards_nom', 'cards', ['nom'])
    op.create_index('ix_cards_encre', 'cards', ['encre'])
    op.create_index('ix_cards_rarete', 'cards', ['rarete'])
    op.create_index('ix_cards_status', 'cards', ['status'])
    op.create_index('idx_card_search', 'cards', ['nom', 'encre', 'rarete'])
    op.create_index('idx_card_status_created', 'cards', ['status', 'created_at'])
    
    # Create card_images table
    op.create_table(
        'card_images',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('card_id', sa.Integer(), nullable=True),
        sa.Column('original_path', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, default='non_traite'),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for card_images table
    op.create_index('ix_card_images_id', 'card_images', ['id'])
    op.create_index('ix_card_images_card_id', 'card_images', ['card_id'])
    op.create_index('ix_card_images_status', 'card_images', ['status'])
    op.create_index('idx_image_status_created', 'card_images', ['status', 'created_at'])
    
    # Create ocr_logs table
    op.create_table(
        'ocr_logs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('card_image_id', sa.Integer(), nullable=False),
        sa.Column('raw_response', sa.Text(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['card_image_id'], ['card_images.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for ocr_logs table
    op.create_index('ix_ocr_logs_id', 'ocr_logs', ['id'])
    op.create_index('ix_ocr_logs_card_image_id', 'ocr_logs', ['card_image_id'])
    op.create_index('idx_ocr_image_created', 'ocr_logs', ['card_image_id', 'created_at'])


def downgrade() -> None:
    """Drop all tables and indexes."""
    
    # Drop indexes first
    op.drop_index('idx_ocr_image_created', table_name='ocr_logs')
    op.drop_index('ix_ocr_logs_card_image_id', table_name='ocr_logs')
    op.drop_index('ix_ocr_logs_id', table_name='ocr_logs')
    
    op.drop_index('idx_image_status_created', table_name='card_images')
    op.drop_index('ix_card_images_status', table_name='card_images')
    op.drop_index('ix_card_images_card_id', table_name='card_images')
    op.drop_index('ix_card_images_id', table_name='card_images')
    
    op.drop_index('idx_card_status_created', table_name='cards')
    op.drop_index('idx_card_search', table_name='cards')
    op.drop_index('ix_cards_status', table_name='cards')
    op.drop_index('ix_cards_rarete', table_name='cards')
    op.drop_index('ix_cards_encre', table_name='cards')
    op.drop_index('ix_cards_nom', table_name='cards')
    op.drop_index('ix_cards_id', table_name='cards')
    
    # Drop tables
    op.drop_table('ocr_logs')
    op.drop_table('card_images')
    op.drop_table('cards')
