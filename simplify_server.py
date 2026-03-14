#!/usr/bin/env python3
import json
import sys
import logging
import warnings
import os

# Suppress warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

from simplify import _load_model, simplify_with_t5, split_sentences
from utils import compute_metrics

# Use absolute path for the local model to avoid huggingface trying to parse it as a hub ID
# when run from a different working directory
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t5-simplifier")

def format_for_dyslexia(simplified_text: str, split_func, use_hyphenation: bool = False) -> str:
    """Imported logic for dyslexia formatting"""
    from dyslexia_mode import format_for_dyslexia
    return format_for_dyslexia(simplified_text, split_func, use_hyphenation)

def format_for_adhd(simplified_text: str) -> str:
    """Imported logic for ADHD formatting"""
    from adhd_mode import format_for_adhd
    return format_for_adhd(simplified_text)

def format_for_autism(simplified_text: str) -> str:
    """Imported logic for autism formatting"""
    from autism_mode import format_for_autism
    return format_for_autism(simplified_text)

def process_text(text: str, mode: str, model_name: str = MODEL_DIR, use_hyphenation: bool = False) -> str:
    """Process text according to the specified mode."""
    # 1. Neural Simplification
    simplified = simplify_with_t5(text, model_name)

    # 2. Mode-Specific Post-Processing
    if mode == "dyslexia":
        return format_for_dyslexia(simplified, split_sentences, use_hyphenation)
    elif mode == "adhd":
        return format_for_adhd(simplified)
    elif mode == "autism":
        return format_for_autism(simplified)

    return simplified

def main():
    # Preload the default model to avoid delays on first request
    try:
        _load_model(MODEL_DIR)
    except Exception as e:
        # Ignore error if model doesn't exist yet
        pass

    # Read from stdin continuously
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)

            # Expected payload: { "text": "...", "mode": "dyslexia", "model": "./t5-simplifier", "useHyphenation": false }
            text = request.get("text", "")
            mode = request.get("mode", "dyslexia")
            use_hyphenation = request.get("useHyphenation", False)

            # Translate the frontend's "./t5-simplifier" to the absolute path
            # Otherwise huggingface throws a validation error when running from a subfolder
            model_name = request.get("model", MODEL_DIR)
            if model_name == "./t5-simplifier":
                model_name = MODEL_DIR

            if not text:
                response = {
                    "error": "No text provided"
                }
            else:
                simplified = process_text(text, mode, model_name, use_hyphenation)
                metrics = compute_metrics(text, simplified)

                # metrics is a nested dict: {'before': {'word_count':...}, 'after': {...}, 'change': {...}}
                response = {
                    "simplified": simplified,
                    "metrics": metrics
                }

            print(json.dumps(response), flush=True)

        except Exception as e:
            error_response = {
                "error": str(e)
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
