#!/usr/bin/env python3
"""CLI tool for text simplification with different accessibility modes."""

import argparse
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Import mode-specific logic
from dyslexia_mode import format_for_dyslexia
from adhd_mode import format_for_adhd
from autism_mode import format_for_autism

# Import shared utilities
from utils import read_input_file, split_sentences, compute_metrics, print_metrics


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


def simplify_with_t5(text: str) -> str:
    """Simplify text using T5-small model.

    Processes sentence by sentence for better results.
    """
    model, tokenizer = _load_model()

    sentences = split_sentences(text)
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


def process_text(text: str, mode: str) -> str:
    """Process text according to the specified mode."""
    # 1. Neural Simplification (Shared)
    simplified = simplify_with_t5(text)

    # 2. Mode-Specific Post-Processing
    if mode == "dyslexia":
        return format_for_dyslexia(simplified, split_sentences)
    elif mode == "adhd":
        return format_for_adhd(simplified)
    elif mode == "autism":
        return format_for_autism(simplified)

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
