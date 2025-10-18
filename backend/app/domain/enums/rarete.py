"""Rarete (Rarity) enum for Lorcana cards."""
from enum import Enum


class Rarete(str, Enum):
    """Available rarities in Lorcana."""
    
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    LEGENDARY = "Legendary"
    ENCHANTED = "Enchanted"
