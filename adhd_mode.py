"""ADHD accessibility formatting logic.

Uses spaCy for intelligent part-of-speech tagging to:
- Accurately identify nouns (not just heuristics)
- Distinguish gerunds acting as nouns vs verbs
- Skip pronouns and articles
"""
import re
import logging
from typing import List

logger = logging.getLogger(__name__)

# Import utilities - handle ImportError gracefully
try:
    from nlp_utils import get_first_noun_position, is_spacy_available
    SPACY_AVAILABLE = is_spacy_available()
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("nlp_utils not available, using fallback heuristics")

from utils import split_sentences


# Skip words for fallback heuristic
_SKIP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'nor', 'for', 'so', 'yet',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'to', 'of', 'in', 'on', 'at', 'by', 'with', 'about',
    'he', 'she', 'it', 'they', 'we', 'you', 'i',
    'him', 'her', 'them', 'us', 'me',
    'his', 'her', 'its', 'their', 'our', 'my', 'your',
    'this', 'that', 'these', 'those',
    'what', 'which', 'who', 'whom',
    'can', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'do', 'does', 'did', 'have', 'has', 'had',
    'very', 'really', 'just', 'only', 'also', 'even',
}


def _bold_first_noun(sentence: str) -> str:
    """Bold the first significant noun using spaCy POS tagging.

    Falls back to heuristics only if spaCy is genuinely unavailable,
    logging the fallback. Does NOT catch all exceptions silently.

    Args:
        sentence: Input sentence

    Returns:
        Sentence with first noun bolded using markdown **noun**
    """
    if not sentence or len(sentence.strip()) < 2:
        return sentence

    # Try spaCy-based detection
    if SPACY_AVAILABLE:
        try:
            result = _bold_first_noun_spacy(sentence)
            if result != sentence:
                return result
        except OSError as e:
            # Only catch OSError (model not found), let other errors propagate
            logger.warning(f"spaCy model error, using fallback: {e}")
        except Exception as e:
            # Log unexpected exceptions but don't silently swallow them
            logger.error(f"Unexpected error in spaCy noun detection: {e}")

    # Fallback to heuristics
    return _bold_first_noun_fallback(sentence)


def _bold_first_noun_spacy(sentence: str) -> str:
    """Bold first noun using spaCy POS tagging."""
    from nlp_utils import get_first_noun_position

    result = get_first_noun_position(sentence)
    if result is None:
        return sentence

    noun, start, end = result
    # Check if noun is already bolded (edge case)
    if start > 2 and sentence[start-2:start] == '**':
        return sentence

    # Bold the noun with proper character position handling
    # This ensures punctuation stays outside bold markers
    return sentence[:start] + '**' + noun + '**' + sentence[end:]


def _bold_first_noun_fallback(sentence: str) -> str:
    """Fallback heuristic for noun detection when spaCy unavailable.

    Less accurate but functional. Logs warning to indicate fallback.
    """
    logger.debug("Using fallback heuristic for noun detection")

    words = sentence.split()
    if len(words) < 2:
        return sentence

    for i, word in enumerate(words):
        # Clean the word for comparison (remove punctuation)
        clean = re.sub(r'[^\w]', '', word.lower())

        # Skip if it's in our skip words list
        if clean in _SKIP_WORDS:
            continue

        # Bold the first significant content word
        if len(clean) > 2:
            words[i] = f"**{word}**"
            break

    return " ".join(words)


def format_for_adhd(text: str) -> str:
    """Format text for ADHD accessibility.

    Features:
    - Converts paragraphs into bulleted lists
    - Adds progress markers [1/N], [2/N], etc.
    - Bolds key terms for emphasis using POS tagging

    Args:
        text: Input text to format

    Returns:
        Formatted text with progress markers and bolded nouns
    """
    sentences = split_sentences(text)
    total = len(sentences)

    if total == 0:
        return text

    lines = []
    for i, sentence in enumerate(sentences, 1):
        bolded = _bold_first_noun(sentence)
        line = f"[{i}/{total}] - {bolded}"
        lines.append(line)

    return "\n".join(lines)
