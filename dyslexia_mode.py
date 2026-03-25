"""Dyslexia accessibility formatting logic."""
import re
from typing import List, Set, Tuple


# Common compound word pairs that should not be split
_COMPOUND_PATTERNS: Set[Tuple[str, str]] = {
    ('black', 'white'),
    ('up', 'down'),
    ('back', 'forth'),
    ('day', 'night'),
    ('left', 'right'),
    ('in', 'out'),
    ('on', 'off'),
    ('top', 'bottom'),
    ('front', 'back'),
    ('high', 'low'),
    ('fast', 'slow'),
    ('big', 'small'),
    ('long', 'short'),
    ('hot', 'cold'),
    ('old', 'new'),
    ('good', 'bad'),
    ('true', 'false'),
    ('yes', 'no'),
}


def _is_compound_pattern(word1: str, word2: str) -> bool:
    """Check if two words form a recognized compound pattern.

    Compound patterns are common word pairs that together
    form a single conceptual unit (e.g., 'black and white').

    Args:
        word1: First word (lowercase)
        word2: Second word (lowercase)

    Returns:
        True if the word pair is a recognized compound pattern
    """
    w1 = word1.lower().strip('.,!?;:')
    w2 = word2.lower().strip('.,!?;:')
    return (w1, w2) in _COMPOUND_PATTERNS or (w2, w1) in _COMPOUND_PATTERNS

def _split_on_conjunctions(sentence: str) -> List[str]:
    """Split sentence on conjunctions and relative clauses.

    Preserves compound patterns like 'black and white' when possible.
    Handles causal relationships by keeping both concepts present.
    """
    # Split on common conjunctions and clause markers
    parts = re.split(
        r'\s*,?\s*\b(and|but|or|nor|for|so|yet|which|that|because|although|though|since|unless|until|when|while|where|how|however|moreover|furthermore|nevertheless|nonetheless|consequently|therefore|thus|hence|often|also)\b\s*',
        sentence,
        flags=re.IGNORECASE
    )

    result = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if not part:
            i += 1
            continue

        # Skip conjunctions and clause markers
        if part.lower() in ('and', 'but', 'or', 'nor', 'for', 'so', 'yet', 'which', 'that',
                          'because', 'although', 'though', 'since', 'unless', 'until', 'when',
                          'while', 'where', 'how', 'however', 'moreover', 'furthermore',
                          'nevertheless', 'nonetheless', 'consequently', 'therefore', 'thus', 'hence'):
            i += 1
            continue

        # Handle 'often' and 'also' as sentence starters
        if part.lower() in ('often', 'also') and i + 1 < len(parts):
            next_part = parts[i + 1].strip() if i + 1 < len(parts) else ''
            if next_part:
                result.append(f"{part.capitalize()} {next_part}")
                i += 2
                continue

        # Default: add the part
        result.append(part)
        i += 1

    # Additional pass: check for compound patterns that were split
    # and merge them back together
    merged_result = []
    skip_next = False
    for i in range(len(result)):
        if skip_next:
            skip_next = False
            continue

        # Check if current part ends with a word that forms a compound
        # with the start of the next part
        if i + 1 < len(result):
            current_words = result[i].split()
            next_words = result[i + 1].split()

            if current_words and next_words:
                last_word = current_words[-1].lower().strip('.,!?;:')
                first_next_word = next_words[0].lower().strip('.,!?;:')

                # If they form a compound pattern, merge them
                if _is_compound_pattern(last_word, first_next_word):
                    # Keep the conjunction "and" between them for compound patterns
                    merged_result.append(f"{result[i]} and {result[i + 1]}")
                    skip_next = True
                    continue

        merged_result.append(result[i])

    return merged_result

def _ensure_sentence_end(sentence: str) -> str:
    """Ensure sentence ends with proper punctuation."""
    sentence = sentence.strip()
    if sentence and sentence[-1] not in '.!?':
        sentence += '.'
    return sentence

def _capitalize_first(sentence: str) -> str:
    """Capitalize first letter of sentence."""
    if sentence:
        return sentence[0].upper() + sentence[1:]
    return sentence

def _is_vowel(char):
    return char.lower() in 'aeiouy'

def _hyphenate_word(word: str) -> str:
    """Insert hyphens into a long word using simple heuristics.

    Uses regex for speed and correctness (avoiding loop duplication bugs).
    Rule 1: Split VC-CV (vowel-consonant-consonant-vowel) -> bet-ter
    Rule 2: Split V-CV (vowel-consonant-vowel) -> ba-sic
    """
    if len(word) < 7:
        return word

    # Use a placeholder to avoid re-splitting already split parts
    # 1. VC-CV Pattern: Split between two consonants surrounded by vowels
    # e.g., "better" -> "bet-ter", "intel" -> "in-tel"
    word = re.sub(r'([aeiouy][^aeiouy])([^aeiouy][aeiouy])', r'\1-\2', word, flags=re.IGNORECASE)

    # 2. V-CV Pattern: Split after vowel if followed by consonant-vowel
    # e.g., "basic" -> "ba-sic"
    # We skip this if it creates very short segments to avoid over-hyphenation
    # word = re.sub(r'([aeiouy])([^aeiouy][aeiouy])', r'\1-\2', word, flags=re.IGNORECASE)

    return word

def _hyphenate_text(text: str) -> str:
    """Apply hyphenation to long words in text."""
    words = text.split(' ')
    processed = []
    for word in words:
        # Check if word contains punctuation
        clean_word = re.sub(r'[^\w\s]', '', word)
        if len(clean_word) > 6:
            # Preserve punctuation by replacing the word part only
            hyphenated = _hyphenate_word(clean_word)
            word = word.replace(clean_word, hyphenated)
        processed.append(word)
    return " ".join(processed)

def format_for_dyslexia(text: str, split_sentences_func, use_hyphenation: bool = False) -> str:
    """Format text for dyslexia accessibility.

    1. Breaks text into short, single-idea sentences.
    2. One sentence per line.
    3. Optionally adds hyphens to long words based on user preference.

    Args:
        text: Input text to format
        split_sentences_func: Function to split text into sentences
        use_hyphenation: If True, adds hyphens to long words (disabled by default per BDA)

    Returns:
        Formatted text with one sentence per paragraph
    """
    sentences = split_sentences_func(text)
    output_lines = []

    for sentence in sentences:
        # Split long sentences on conjunctions
        parts = _split_on_conjunctions(sentence)

        for part in parts:
            # Filter out very short fragments (less than 2 words)
            # But keep meaningful single-word sentences if they exist
            word_count = len(part.split())
            if word_count < 2:
                continue

            cleaned = _capitalize_first(part)
            cleaned = _ensure_sentence_end(cleaned)

            # Apply hyphenation based on user preference
            # Note: Hyphenation is disabled by default as per BDA guidelines
            # which state that hyphenation disrupts word-shape recognition
            # that dyslexic readers rely on.
            if use_hyphenation:
                cleaned = _hyphenate_text(cleaned)

            output_lines.append(cleaned)

    return "\n\n".join(output_lines)
