"""Seed script to populate the database with test data."""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.base import Base
from backend.app.models.card import Card
from backend.app.models.card_image import CardImage
from backend.app.models.ocr_log import OCRLog

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../lorcana_cards.db")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_database():
    """
    Seed the database with test data.
    
    Creates sample cards across different inks, rarities, and statuses
    to facilitate development and testing.
    """
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Test data: Sample Lorcana cards
        test_cards = [
            {
                "nom": "Mickey Mouse",
                "sous_titre": "Brave Little Tailor",
                "encre": "Steel",
                "encrable": True,
                "cout": 5,
                "force": 3,
                "volonte": 4,
                "lore": 2,
                "mots_cles": "Hero, Bodyguard",
                "texte": "GIANT SLAYER: When you play this character, chosen opposing character gets -4 strength this turn.",
                "texte_fr": "TUEUR DE GÉANT : Lorsque vous jouez ce personnage, un personnage adverse choisi gagne -4 en force ce tour.",
                "rarete": "Rare",
                "status": "valide",
            },
            {
                "nom": "Elsa",
                "sous_titre": "Ice Queen",
                "encre": "Sapphire",
                "encrable": True,
                "cout": 6,
                "force": 4,
                "volonte": 4,
                "lore": 3,
                "mots_cles": "Storyborn, Queen",
                "texte": "LET IT GO: When you play this character, you may return an item card from your discard to your hand.",
                "texte_fr": "LIBÉRÉE, DÉLIVRÉE : Lorsque vous jouez ce personnage, vous pouvez récupérer une carte objet depuis votre défausse.",
                "rarete": "Super Rare",
                "status": "valide",
            },
            {
                "nom": "Stitch",
                "sous_titre": "Carefree Surfer",
                "encre": "Emerald",
                "encrable": True,
                "cout": 4,
                "force": 2,
                "volonte": 5,
                "lore": 2,
                "mots_cles": "Hero, Alien",
                "texte": "OHANA: While you have 2 or more characters in play, this character gets +2 Lore.",
                "texte_fr": "OHANA : Tant que vous avez 2 personnages ou plus en jeu, ce personnage gagne +2 en connaissance.",
                "rarete": "Uncommon",
                "status": "valide",
            },
            {
                "nom": "Aladdin",
                "sous_titre": "Street Rat",
                "encre": "Amber",
                "encrable": False,
                "cout": 1,
                "force": 1,
                "volonte": 2,
                "lore": 1,
                "mots_cles": "Storyborn, Hero",
                "texte": "IMPROVISE: When you play this character, you may draw a card, then choose and discard a card.",
                "texte_fr": "IMPROVISER : Lorsque vous jouez ce personnage, vous pouvez piocher une carte, puis choisir et défausser une carte.",
                "rarete": "Common",
                "status": "attente_validation",
            },
            {
                "nom": "Maleficent",
                "sous_titre": "Monstrous Dragon",
                "encre": "Amethyst",
                "encrable": True,
                "cout": 9,
                "force": 7,
                "volonte": 7,
                "lore": 2,
                "mots_cles": "Storyborn, Villain, Dragon",
                "texte": "FIRE BREATH: Whenever this character quests, deal 2 damage to each opposing character.",
                "texte_fr": "SOUFFLE DE FEU : Chaque fois que ce personnage se lance dans une quête, infligez 2 dégâts à chaque personnage adverse.",
                "rarete": "Legendary",
                "status": "valide",
            },
            {
                "nom": "Simba",
                "sous_titre": "Future King",
                "encre": "Ruby",
                "encrable": True,
                "cout": 3,
                "force": 2,
                "volonte": 3,
                "lore": 1,
                "mots_cles": "Storyborn, Hero, Prince",
                "texte": "I CAN'T WAIT TO BE KING: When you play this character, if you have 2 or more other characters in play, chosen opposing character can't quest during their next turn.",
                "texte_fr": "JE RÊVE D'ÊTRE ROI : Lorsque vous jouez ce personnage, si vous avez 2 autres personnages ou plus en jeu, un personnage adverse choisi ne peut pas se lancer dans une quête pendant son prochain tour.",
                "rarete": "Rare",
                "status": "valide",
            },
        ]
        
        # Insert cards
        for card_data in test_cards:
            card = Card(**card_data)
            db.add(card)
        
        db.commit()
        print(f"✅ Created {len(test_cards)} test cards")
        
        # Create some test card_images
        cards = db.query(Card).all()
        
        test_images = [
            {
                "card_id": cards[0].id,
                "original_path": f"uploads/2025-10-17/mickey_brave_tailor.jpg",
                "status": "valide",
            },
            {
                "card_id": cards[1].id,
                "original_path": f"uploads/2025-10-17/elsa_ice_queen.jpg",
                "status": "valide",
            },
            {
                "card_id": None,  # Image without card yet
                "original_path": f"uploads/2025-10-17/pending_card_001.jpg",
                "status": "non_traite",
            },
            {
                "card_id": None,  # Image in processing
                "original_path": f"uploads/2025-10-17/pending_card_002.jpg",
                "status": "en_cours",
            },
            {
                "card_id": cards[3].id,  # Aladdin waiting validation
                "original_path": f"uploads/2025-10-17/aladdin_street_rat.jpg",
                "status": "attente_validation",
            },
        ]
        
        for image_data in test_images:
            card_image = CardImage(**image_data)
            db.add(card_image)
        
        db.commit()
        print(f"✅ Created {len(test_images)} test card images")
        
        # Create some OCR logs
        images = db.query(CardImage).all()
        
        test_logs = [
            {
                "card_image_id": images[0].id,
                "raw_response": '{"nom": "Mickey Mouse", "sous_titre": "Brave Little Tailor", "encre": "Steel", "cout": 5}',
                "error_message": None,
            },
            {
                "card_image_id": images[1].id,
                "raw_response": '{"nom": "Elsa", "sous_titre": "Ice Queen", "encre": "Sapphire", "cout": 6}',
                "error_message": None,
            },
            {
                "card_image_id": images[3].id,
                "raw_response": None,
                "error_message": "Groq API timeout after 30 seconds",
            },
        ]
        
        for log_data in test_logs:
            ocr_log = OCRLog(**log_data)
            db.add(ocr_log)
        
        db.commit()
        print(f"✅ Created {len(test_logs)} OCR logs")
        
        print("🎉 Database seeding completed successfully!")
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"  - Total cards: {db.query(Card).count()}")
        print(f"  - Cards validated: {db.query(Card).filter(Card.status == 'valide').count()}")
        print(f"  - Cards awaiting validation: {db.query(Card).filter(Card.status == 'attente_validation').count()}")
        print(f"  - Total images: {db.query(CardImage).count()}")
        print(f"  - Images not processed: {db.query(CardImage).filter(CardImage.status == 'non_traite').count()}")
        print(f"  - Total OCR logs: {db.query(OCRLog).count()}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_database():
    """
    Clear all data from the database.
    
    Warning: This will delete all cards, images, and logs!
    """
    db = SessionLocal()
    
    try:
        print("🗑️  Clearing database...")
        
        # Delete in order (respecting foreign keys)
        db.query(OCRLog).delete()
        db.query(CardImage).delete()
        db.query(Card).delete()
        
        db.commit()
        print("✅ Database cleared successfully!")
        
    except Exception as e:
        print(f"❌ Error during clearing: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear the database before seeding"
    )
    parser.add_argument(
        "--clear-only",
        action="store_true",
        help="Only clear the database, don't seed"
    )
    
    args = parser.parse_args()
    
    if args.clear_only:
        clear_database()
    elif args.clear:
        clear_database()
        seed_database()
    else:
        seed_database()
