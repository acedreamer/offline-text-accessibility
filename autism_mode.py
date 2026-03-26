"""Autism accessibility formatting logic.

Handles:
- Idiom replacement with per-match context awareness
- Jargon simplification
- Literal interpretation support
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Lazy-loaded maps
_IDIOM_MAP: Optional[Dict] = None
_JARGON_MAP: Optional[Dict] = None

# Context patterns that suggest literal usage
_LITERAL_CONTEXTS: Dict[str, List[str]] = {
    'break a leg': ['fell', 'injury', 'hurt', 'broken', 'doctor', 'hospital', 'pain', 'broke', 'leg', 'accident', 'fall', 'fracture'],
    'kick the bucket': ['water', 'yard', 'bucket', 'spilled', 'carried', 'floor', 'child', 'kid', 'kick', 'kicked', 'pail', 'container'],
    'hit the nail': ['hammer', 'wood', 'construction', 'finger', 'thumb', 'hit', 'nail', 'head', 'tool', 'build'],
    'spill the beans': ['cooking', 'kitchen', 'floor', 'mess', 'cooking', 'jar', 'can', 'drop', 'spilled'],
    'let the cat out': ['pet', 'door', 'escaped', 'animal', 'ran', 'outside', 'bag', 'carrier', 'mouse'],
    'cold feet': ['wash', 'water', 'winter', 'freeze', 'ice', 'temperature', 'socks', 'warm', 'cold', 'outside', 'snow'],
    'piece of cake': ['eat', 'bakery', 'slice', 'dessert', 'baked', 'recipe', 'chocolate', 'birthday'],
    'raining cats and dogs': ['animal', 'pet', 'veterinarian', 'pound'],
    'apple of my eye': ['fruit', 'eat', 'doctor', 'healthy', 'pie'],
    'break the ice': ['freezer', 'drink', 'cube', 'cold', 'melt', 'frozen'],
    'burning the midnight oil': ['lamp', 'engine', 'car', 'fuel', 'gas', 'cooking', 'fry'],
    'when pigs fly': ['farm', 'animal', 'zoo', 'pet'],
}

def _load_idiom_map() -> Dict:
    """Lazily load idiom mappings from JSON file."""
    global _IDIOM_MAP
    if _IDIOM_MAP is None:
        try:
            path = Path(__file__).parent / "idiom_map.json"
            with open(path, 'r') as f:
                data = json.load(f)
                # Filter out metadata keys
                _IDIOM_MAP = {k: v for k, v in data.items() if not k.startswith('__')}
        except FileNotFoundError:
            logger.warning("idiom_map.json not found, using empty map")
            _IDIOM_MAP = {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in idiom_map.json: {e}")
            _IDIOM_MAP = {}
    return _IDIOM_MAP


def _load_jargon_map() -> Dict:
    """Lazily load jargon mappings from JSON file."""
    global _JARGON_MAP
    if _JARGON_MAP is None:
        try:
            path = Path(__file__).parent / "jargon_map.json"
            with open(path, 'r') as f:
                data = json.load(f)
                _JARGON_MAP = {k: v for k, v in data.items() if not k.startswith('__')}
        except FileNotFoundError:
            logger.warning("jargon_map.json not found, using empty map")
            _JARGON_MAP = {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in jargon_map.json: {e}")
            _JARGON_MAP = {}
    return _JARGON_MAP


def get_idiom_map() -> Dict:
    """Public accessor for idiom map (for testing)."""
    return _load_idiom_map()


def get_jargon_map() -> Dict:
    """Public accessor for jargon map (for testing)."""
    return _load_jargon_map()


def _get_match_context(text: str, match_start: int, match_end: int, window: int = 50) -> str:
    """Get text surrounding a specific match for context analysis, excluding the match itself."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    return text[start:match_start] + " " + text[match_end:end]


def _is_idiom_in_context(text: str, idiom: str, match_start: int, match_end: int) -> bool:
    """Check if a specific occurrence of an idiom is used idiomatically."""
    if idiom not in _LITERAL_CONTEXTS:
        return True

    context = _get_match_context(text, match_start, match_end)
    context_lower = context.lower()

    literal_words = _LITERAL_CONTEXTS.get(idiom, [])
    for word in literal_words:
        if word in context_lower:
            return False

    return True


def _replace_idioms(text: str) -> str:
    """Replace idioms with literal meanings (per-match context-aware)."""
    idiom_map = _load_idiom_map()
    if not idiom_map:
        return text

    result = text
    for idiom, literal in idiom_map.items():
        pattern = rf'\b{re.escape(idiom)}\b'
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        for match in reversed(matches):
            if _is_idiom_in_context(result, idiom, match.start(), match.end()):
                result = result[:match.start()] + f"**{literal}**" + result[match.end():]

    return result


def _replace_jargon(text: str) -> str:
    """Replace academic/medical jargon with plain language."""
    jargon_map = _load_jargon_map()
    if not jargon_map:
        return text

    result = text
    for term, plain in jargon_map.items():
        if term.isupper() or (len(term) > 1 and any(c.isupper() for c in term[1:])):
            pattern = rf'(?<!\w){re.escape(term)}(?!\w)'
            result = re.sub(pattern, f"**{plain}**", result)
        else:
            pattern = rf'\b{re.escape(term)}\b'
            result = re.sub(pattern, f"**{plain}**", result, flags=re.IGNORECASE)

    return result


def format_for_autism(text: str) -> str:
    """Format text for autism/literal clarity accessibility."""
    if not text or not text.strip():
        return text

    text = _replace_idioms(text)
    text = _replace_jargon(text)
    return text
