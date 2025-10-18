"""Encre (Ink) enum for Lorcana cards."""
from enum import Enum


class Encre(str, Enum):
    """Available ink colors in Lorcana."""
    
    AMBER = "Amber"
    AMETHYST = "Amethyst"
    EMERALD = "Emerald"
    RUBY = "Ruby"
    SAPPHIRE = "Sapphire"
    STEEL = "Steel"
