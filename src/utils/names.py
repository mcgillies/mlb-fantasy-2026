"""
Player name matching utilities.

Handles fuzzy matching, name normalization, and ID-based lookups
to avoid the name collision issues from the 2025 version.
"""

import unidecode
from rapidfuzz import fuzz, process


def normalize_name(name):
    """Normalize a player name (unicode, strip, lowercase)."""
    return unidecode.unidecode(name).strip().lower()


def fuzzy_match_name(name, candidates, threshold=85):
    """
    Find the best fuzzy match for a player name.

    Args:
        name: Name to match.
        candidates: List of candidate names.
        threshold: Minimum similarity score (0-100).

    Returns:
        Best match string or None.
    """
    result = process.extractOne(name, candidates, scorer=fuzz.ratio)
    if result and result[1] >= threshold:
        return result[0]
    return None
