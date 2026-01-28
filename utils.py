"""Shared utility functions and metrics."""
import re
import sys
from pathlib import Path

def read_input_file(file_path: str) -> str:
    """Read and return contents of the input file."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")

def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def get_words(text: str) -> list[str]:
    """Extract words from text."""
    return re.findall(r'[a-zA-Z]+', text)

def count_syllables(word: str) -> int:
    """Count syllables in a word using a simple heuristic."""
    word = word.lower().strip()
    if not word:
        return 0

    # Remove trailing e
    if word.endswith('e') and len(word) > 2:
        word = word[:-1]

    # Count vowel groups
    vowels = 'aeiou'
    count = 0
    prev_is_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    return max(1, count)

def compute_avg_sentence_length(text: str) -> float:
    """Compute average words per sentence."""
    sentences = split_sentences(text)
    if not sentences:
        return 0.0

    words = get_words(text)
    return len(words) / len(sentences)

def compute_flesch_reading_ease(text: str) -> float:
    """Compute Flesch Reading Ease score."""
    sentences = split_sentences(text)
    words = get_words(text)

    if not sentences or not words:
        return 0.0

    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return round(score, 2)

def compute_word_count(text: str) -> int:
    """Count total words in text."""
    return len(get_words(text))

def compute_metrics(before: str, after: str) -> dict:
    """Compute comparison metrics between original and simplified text."""
    return {
        "before": {
            "word_count": compute_word_count(before),
            "avg_sentence_length": round(compute_avg_sentence_length(before), 2),
            "flesch_reading_ease": compute_flesch_reading_ease(before),
        },
        "after": {
            "word_count": compute_word_count(after),
            "avg_sentence_length": round(compute_avg_sentence_length(after), 2),
            "flesch_reading_ease": compute_flesch_reading_ease(after),
        },
        "change": {
            "word_count": compute_word_count(after) - compute_word_count(before),
            "avg_sentence_length": round(
                compute_avg_sentence_length(after) - compute_avg_sentence_length(before), 2
            ),
            "flesch_reading_ease": round(
                compute_flesch_reading_ease(after) - compute_flesch_reading_ease(before), 2
            ),
        },
    }

def print_metrics(metrics: dict) -> None:
    """Print metrics in a readable format."""
    print("\n--- Readability Metrics ---")
    print(f"{'Metric':<25} {'Before':>10} {'After':>10} {'Change':>10}")
    print("-" * 57)
    print(f"{'Word count':<25} {metrics['before']['word_count']:>10} {metrics['after']['word_count']:>10} {metrics['change']['word_count']:>+10}")
    print(f"{'Avg sentence length':<25} {metrics['before']['avg_sentence_length']:>10.2f} {metrics['after']['avg_sentence_length']:>10.2f} {metrics['change']['avg_sentence_length']:>+10.2f}")
    print(f"{'Flesch Reading Ease':<25} {metrics['before']['flesch_reading_ease']:>10.2f} {metrics['after']['flesch_reading_ease']:>10.2f} {metrics['change']['flesch_reading_ease']:>+10.2f}")
    print("-" * 57)
