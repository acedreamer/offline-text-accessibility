#!/usr/bin/env python3
"""CLI tool for text simplification with different accessibility modes."""

import argparse
import re
import sys
from pathlib import Path

from transformers import T5ForConditionalGeneration, T5Tokenizer


# Global model and tokenizer (loaded once)
_model = None
_tokenizer = None


def _load_model():
    """Load T5 model and tokenizer if not already loaded."""
    global _model, _tokenizer
    if _model is None:
        _tokenizer = T5Tokenizer.from_pretrained("t5-small")
        _model = T5ForConditionalGeneration.from_pretrained("t5-small")
        _model.eval()
    return _model, _tokenizer


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


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


def format_for_dyslexia(text: str) -> str:
    """Format text for dyslexia accessibility.

    Breaks text into short, single-idea sentences.
    One sentence per line for reduced cognitive load.
    """
    sentences = _split_sentences(text)
    output_lines = []

    for sentence in sentences:
        # Split long sentences on conjunctions
        parts = _split_on_conjunctions(sentence)

        for part in parts:
            if len(part.split()) < 3:
                continue
            cleaned = _capitalize_first(part)
            cleaned = _ensure_sentence_end(cleaned)
            output_lines.append(cleaned)

    return "\n\n".join(output_lines)


# --- Evaluation Metrics ---

def _count_syllables(word: str) -> int:
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


def _get_words(text: str) -> list[str]:
    """Extract words from text."""
    return re.findall(r'[a-zA-Z]+', text)


def compute_avg_sentence_length(text: str) -> float:
    """Compute average words per sentence."""
    sentences = _split_sentences(text)
    if not sentences:
        return 0.0

    words = _get_words(text)
    return len(words) / len(sentences)


def compute_flesch_reading_ease(text: str) -> float:
    """Compute Flesch Reading Ease score.

    Score interpretation:
        90-100: Very easy (5th grade)
        80-89:  Easy (6th grade)
        70-79:  Fairly easy (7th grade)
        60-69:  Standard (8th-9th grade)
        50-59:  Fairly difficult (10th-12th grade)
        30-49:  Difficult (college)
        0-29:   Very difficult (college graduate)
    """
    sentences = _split_sentences(text)
    words = _get_words(text)

    if not sentences or not words:
        return 0.0

    total_syllables = sum(_count_syllables(w) for w in words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return round(score, 2)


def compute_word_count(text: str) -> int:
    """Count total words in text."""
    return len(_get_words(text))


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


def simplify_with_t5(text: str) -> str:
    """Simplify text using T5-small model.

    Processes sentence by sentence for better results.

    Args:
        text: Input text to simplify.

    Returns:
        Simplified text.
    """
    model, tokenizer = _load_model()

    sentences = _split_sentences(text)
    simplified = []

    for sentence in sentences:
        input_text = f"summarize: {sentence}"
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=128,
            num_beams=4,
            length_penalty=1.0,
            early_stopping=True,
        )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        simplified.append(result)

    return " ".join(simplified)


def read_input_file(file_path: str) -> str:
    """Read and return contents of the input file."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def process_text(text: str, mode: str) -> str:
    """Process text according to the specified mode."""
    simplified = simplify_with_t5(text)

    if mode == "dyslexia":
        return format_for_dyslexia(simplified)

    return simplified


def main():
    parser = argparse.ArgumentParser(
        description="Simplify text for different accessibility needs."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input text file"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["dyslexia", "adhd", "autism"],
        help="Accessibility mode for text processing"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show readability metrics (before vs after)"
    )

    args = parser.parse_args()

    text = read_input_file(args.input)
    result = process_text(text, args.mode)
    print(result)

    if args.metrics:
        metrics = compute_metrics(text, result)
        print_metrics(metrics)


if __name__ == "__main__":
    main()
