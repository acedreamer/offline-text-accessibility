"""Dyslexia accessibility formatting logic."""
import re

def _split_on_conjunctions(sentence: str) -> list[str]:
    """Split sentence on conjunctions and relative clauses."""
    # Split on common conjunctions and clause markers
    parts = re.split(r'\s*,?\s*\b(and|but|which|that|because|although|however|often|also)\b\s*', sentence, flags=re.IGNORECASE)

    result = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part and part.lower() not in ('and', 'but', 'which', 'that', 'because', 'although', 'however', 'often', 'also'):
            result.append(part)
        elif part.lower() in ('often', 'also') and i + 1 < len(parts):
            # Keep these as sentence starters
            next_part = parts[i + 1].strip() if i + 1 < len(parts) else ''
            if next_part:
                result.append(f"{part.capitalize()} {next_part}")
                i += 1
        i += 1

    return result

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

def format_for_dyslexia(text: str, split_sentences_func) -> str:
    """Format text for dyslexia accessibility.

    1. Breaks text into short, single-idea sentences.
    2. One sentence per line.
    3. Adds hyphens to long words (NEW).
    """
    sentences = split_sentences_func(text)
    output_lines = []

    for sentence in sentences:
        # Split long sentences on conjunctions
        parts = _split_on_conjunctions(sentence)

        for part in parts:
            if len(part.split()) < 3:
                continue
            cleaned = _capitalize_first(part)
            cleaned = _ensure_sentence_end(cleaned)

            # Apply hyphenation
            cleaned = _hyphenate_text(cleaned)

            output_lines.append(cleaned)

    return "\n\n".join(output_lines)
