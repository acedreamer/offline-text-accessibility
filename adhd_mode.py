"""ADHD accessibility formatting logic."""
import re
from utils import split_sentences


def _bold_first_noun(sentence: str) -> str:
    """Bold the first significant word (simple heuristic)."""
    words = sentence.split()
    if len(words) < 2:
        return sentence

    # Skip common articles/prepositions, bold first content word
    skip_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'on', 'at'}
    for i, word in enumerate(words):
        clean = re.sub(r'[^\w]', '', word.lower())
        if clean not in skip_words and len(clean) > 2:
            words[i] = f"**{word}**"
            break

    return " ".join(words)


def format_for_adhd(text: str) -> str:
    """Format text for ADHD accessibility.

    Features:
    - Converts paragraphs into bulleted lists
    - Adds progress markers [1/N], [2/N], etc.
    - Bolds key terms for emphasis
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
