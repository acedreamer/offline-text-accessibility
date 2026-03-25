"""Shared NLP utilities using spaCy for POS tagging and NER.

This module provides:
- POS tagging for intelligent word classification
- Noun extraction for ADHD mode
- Named entity recognition for proper noun handling
"""
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

# Lazy-loaded spaCy model
_nlp = None


def _get_nlp():
    """Lazy load spaCy model.

    Raises:
        OSError: If spaCy model is not installed.
    """
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def is_spacy_available() -> bool:
    """Check if spaCy model is available without raising."""
    try:
        _get_nlp()
        return True
    except (ImportError, OSError) as e:
        logger.warning(f"spaCy model not available: {e}")
        return False


def get_pos_tags(text: str) -> List[Tuple[str, str]]:
    """Get POS tags for all tokens in text.

    Returns list of (token, tag) tuples.
    """
    nlp = _get_nlp()
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]


def extract_nouns(text: str) -> List[str]:
    """Extract all nouns from text.

    Includes both common nouns (NOUN) and proper nouns (PROPN).
    """
    nlp = _get_nlp()
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]


def get_first_noun(text: str, skip_proper: bool = False) -> Optional[str]:
    """Get the first noun in text.

    Args:
        text: Input text
        skip_proper: If True, skip proper nouns (names, places)

    Returns:
        First noun text, or None if no nouns found
    """
    nlp = _get_nlp()
    doc = nlp(text)

    for token in doc:
        if token.pos_ == "NOUN":
            return token.text
        if not skip_proper and token.pos_ == "PROPN":
            return token.text

    return None


def get_first_noun_position(text: str) -> Optional[Tuple[str, int, int]]:
    """Get the first noun with its character positions.

    Returns:
        Tuple of (noun_text, start_char, end_char) or None
    """
    nlp = _get_nlp()
    doc = nlp(text)

    for token in doc:
        if token.pos_ in ("NOUN", "PROPN"):
            return (token.text, token.idx, token.idx + len(token.text))

    return None
