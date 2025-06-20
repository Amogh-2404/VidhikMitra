"""Simple content moderation utilities."""

import re

BAD_WORDS = {'kill', 'attack', 'bomb'}


def moderate_query(text: str) -> bool:
    """Return False if text contains abusive content."""
    lower = text.lower()
    if any(bad in lower for bad in BAD_WORDS):
        return False
    return True
