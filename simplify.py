#!/usr/bin/env python3
"""CLI tool for text simplification with different accessibility modes."""

import argparse
import os
import warnings
import logging

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

from transformers import T5ForConditionalGeneration, T5Tokenizer, logging as hf_logging
from transformers.utils import logging as hf_utils_logging

hf_logging.set_verbosity_error()
hf_utils_logging.disable_progress_bar()

# Import mode-specific logic
from dyslexia_mode import format_for_dyslexia
from adhd_mode import format_for_adhd
from autism_mode import format_for_autism

# Import shared utilities
from utils import read_input_file, split_sentences, compute_metrics, print_metrics


# Cache for loaded models
_models = {}


def _select_by_task_complexity(text: str) -> str:
    """Select model based on text complexity."""
    words = text.split()
    if not words:
        return "./t5-simplifier"

    avg_word_len = sum(len(w) for w in words) / len(words)

    # Heuristic: longer words = more complex = needs better model
    if avg_word_len > 6 or len(words) > 200:
        return "t5-medium"
    return "./t5-simplifier"


def _select_by_device() -> str:
    """Select model based on available system RAM."""
    try:
        import psutil
        available_gb = psutil.virtual_memory().available / (1024**3)

        # t5-medium needs ~2GB RAM for comfortable operation
        if available_gb > 4:
            return "t5-medium"
        return "./t5-simplifier"
    except ImportError:
        # psutil not available, default to fine-tuned model
        return "./t5-simplifier"


def _select_model(choice: str, text: str) -> str:
    """Determine which model to use."""
    if choice == "small":
        return "./t5-simplifier"
    elif choice == "medium":
        return "t5-medium"
    elif choice == "auto-task":
        return _select_by_task_complexity(text)
    elif choice == "auto-device":
        return _select_by_device()
    return "./t5-simplifier"  # default


def _load_model(model_name: str):
    """Load specified T5 model."""
    if model_name not in _models:
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)
        model.eval()
        _models[model_name] = (model, tokenizer)
    return _models[model_name]


def simplify_with_t5(text: str, model_name: str = "./t5-simplifier") -> str:
    """Simplify text using T5 model.

    Processes sentence by sentence for better results.
    """
    model, tokenizer = _load_model(model_name)

    sentences = split_sentences(text)
    simplified = []

    for sentence in sentences:
        input_text = f"simplify: {sentence}"
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=128,
            num_beams=4,
            length_penalty=0.8,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        simplified.append(result)

    return " ".join(simplified)


def process_text(text: str, mode: str, model_name: str = "t5-small") -> str:
    """Process text according to the specified mode."""
    # 1. Neural Simplification (Shared)
    simplified = simplify_with_t5(text, model_name)

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
        "--model",
        choices=["small", "medium", "auto-task", "auto-device"],
        default="small",
        help="Model to use: small (fast), medium (better quality), auto-task (based on complexity), auto-device (based on RAM)"
    )
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Show readability metrics (before vs after)"
    )

    args = parser.parse_args()

    text = read_input_file(args.input)

    # Select appropriate model
    model_name = _select_model(args.model, text)

    result = process_text(text, args.mode, model_name)
    print(result)

    if args.metrics:
        metrics = compute_metrics(text, result)
        print_metrics(metrics)


if __name__ == "__main__":
    main()
