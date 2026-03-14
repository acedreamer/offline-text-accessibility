"""ADHD accessibility formatting logic."""
import re
from utils import split_sentences


def _bold_first_noun(sentence: str) -> str:
    """Bold the first significant word (enhanced heuristic)."""
    words = sentence.split()
    if len(words) < 2:
        return sentence

    # Expanded skip words including more articles, prepositions, and common weak words
    skip_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'nor', 'for', 'so', 'yet',
        'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'about',
        'against', 'between', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'up', 'down', 'in', 'out', 'on',
        'off', 'over', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
        'has', 'have', 'had', 'having', 'do', 'does', 'did', 'doing',
        'would', 'could', 'should', 'may', 'might', 'must', 'shall'
    }

    # Simple heuristic to avoid bolding words that look like verbs based on common endings
    verb_endings = {'ing', 'ed', 'es', 's'}

    for i, word in enumerate(words):
        # Clean the word for comparison (remove punctuation)
        clean = re.sub(r'[^\w]', '', word.lower())

        # Skip if it's in our skip words list
        if clean in skip_words:
            continue

        # Skip if it looks like a verb (simple heuristic)
        if any(clean.endswith(ending) for ending in verb_endings) and len(clean) > 3:
            continue

        # Bold the first significant content word that passes our filters
        if len(clean) > 2:  # Ensure it's a meaningful word
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
