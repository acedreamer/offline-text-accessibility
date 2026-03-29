#!/usr/bin/env python3
"""CLI tool for text simplification with different accessibility modes."""

import argparse
import os
import warnings
import logging
import re
import json
from pathlib import Path

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
from autism_mode import format_for_autism, _load_idiom_map, _load_jargon_map

# Import shared utilities
from utils import read_input_file, split_sentences, compute_metrics, print_metrics, correct_spelling

# Preprocessing functions for idiom/jargon replacement and homophone correction
def _preprocess_text(text: str) -> str:
    """Apply preprocessing steps to reduce model workload:
    1. Replace idioms with literal meanings (simplifies complex expressions)
    2. Replace jargon with plain language (reduces cognitive load)
    3. Correct spelling/homophones (helps model understand input better)
    """
    if not text or not text.strip():
        return text

    # 1. Replace idioms (using autism mode's context-aware replacement)
    processed = text
    idiom_map = _load_idiom_map()
    if idiom_map:
        result = processed
        for idiom, literal in idiom_map.items():
            pattern = rf'\b{re.escape(idiom)}\b'
            matches = list(re.finditer(pattern, result, re.IGNORECASE))
            for match in reversed(matches):
                # Simple context check - could be enhanced with autism_mode's logic
                # For preprocessing, we'll apply broadly to simplify input for model
                result = result[:match.start()] + f"{literal}" + result[match.end():]
        processed = result

    # 2. Replace jargon (using autism mode's logic)
    jargon_map = _load_jargon_map()
    if jargon_map:
        result = processed
        for term, plain in jargon_map.items():
            if term.isupper() or (len(term) > 1 and any(c.isupper() for c in term[1:])):
                pattern = rf'(?<!\w){re.escape(term)}(?!\w)'
                result = re.sub(pattern, f"{plain}", result)
            else:
                pattern = rf'\b{re.escape(term)}\b'
                result = re.sub(pattern, f"{plain}", result, flags=re.IGNORECASE)
        processed = result

    # 3. Correct spelling and homophones
    processed = correct_spelling(processed)

    return processed


# Cache for loaded models with size limit to prevent memory leaks
_models = {}
_MAX_MODEL_CACHE_SIZE = 3


def _select_by_task_complexity(text: str) -> str:
    """Select model based on text complexity."""
    words = text.split()
    if not words:
        return "./t5"

    avg_word_len = sum(len(w) for w in words) / len(words)

    # Heuristic: longer words = more complex = needs better model
    if avg_word_len > 6 or len(words) > 200:
        return "t5-medium"
    return "./t5"


def _select_by_device() -> str:
    """Select model based on available system RAM."""
    try:
        import psutil
        available_gb = psutil.virtual_memory().available / (1024**3)

        # t5-medium needs ~2GB RAM for comfortable operation
        if available_gb > 4:
            return "t5-medium"
        return "./t5"
    except ImportError:
        # psutil not available, default to fine-tuned model
        return "./t5"


def _select_model(choice: str, text: str) -> str:
    """Determine which model to use."""
    if choice == "small":
        return "./t5"
    elif choice == "medium":
        return "t5-medium"
    elif choice == "auto-task":
        return _select_by_task_complexity(text)
    elif choice == "auto-device":
        return _select_by_device()
    return "./t5" # default


def _load_model(model_name: str):
    """Load specified T5 model with error handling and cache management."""
    if model_name not in _models:
        try:
            tokenizer = T5Tokenizer.from_pretrained(model_name)
            model = T5ForConditionalGeneration.from_pretrained(model_name)
            model.eval()
            _models[model_name] = (model, tokenizer)

            # Limit cache size to prevent memory leaks
            if len(_models) > _MAX_MODEL_CACHE_SIZE:
                # Remove the oldest entry (simple FIFO approach)
                oldest_key = next(iter(_models))
                del _models[oldest_key]

        except Exception as e:
            logging.error(f"Failed to load model {model_name}: {str(e)}")
            # Fallback to a smaller model or raise informative error
            if model_name != "./t5": # Avoid infinite recursion
                logging.info(f"Falling back to base t5-simplifier model from {model_name}")
                return _load_model("./t5")
            raise RuntimeError(f"Could not load any model: {str(e)}")
    return _models[model_name]


# ACCESS control token profiles for neurodivergent simplification
# Format: <LengthRatio_X> <DepDepth_Y> <WordRank_Z> <CCR_W>
# Lower numbers = more aggressive transformation
ACCESS_PROFILES = {
    "dyslexia": "<LengthRatio_5> <DepDepth_2> <WordRank_2> <CCR_5>",
    "adhd": "<LengthRatio_2> <DepDepth_2> <WordRank_5> <CCR_5>",
    "autism": "<LengthRatio_5> <DepDepth_4> <WordRank_5> <CCR_2>",
    "default": "<LengthRatio_5> <DepDepth_5> <WordRank_5> <CCR_5>",
}


def simplify_with_t5(text: str, model_name: str = "./t5", mode: str = None) -> str:
    """Simplify text using T5 model with ACCESS control tokens.

    Preprocesses text to correct spelling/homophones and replace idioms/jargon
    before applying control-token guided simplification.
    Processes sentence by sentence for better results.
    Uses control token prefixes for neurodivergent-specific simplification.
    """
    import torch

    model, tokenizer = _load_model(model_name)

    # Preprocess text to reduce model workload:
    # - Correct spelling/homophones
    # - Replace idioms with literal meanings
    # - Replace jargon with plain language
    processed_text = _preprocess_text(text)

    # Get the correct ACCESS tokens for the requested mode
    prefix = ACCESS_PROFILES.get(mode, ACCESS_PROFILES["default"])

    sentences = split_sentences(processed_text)
    simplified_sentences = []

    for sentence in sentences:
        # Construct the exact prompt the model expects
        input_text = f"{prefix} simplify: {sentence}"

        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            max_length=256,
            truncation=True
        )

        # --- THE FIX: Calculate dynamic length constraints ---
        # Count how many tokens are in the input sentence (excluding the prefix)
        # We want to force the model to keep at least 75% to 85% of the original length
        # to prevent it from deleting dependent clauses like "to avoid stomach upset".
        raw_sentence_tokens = len(tokenizer.encode(sentence))

        # Adjust minimum length preservation based on the mode
        if mode == "adhd":
            # ADHD mode: high compression allowed, chunking is good
            min_out_len = int(raw_sentence_tokens * 0.5)
            len_penalty = 1.0
        elif mode == "autism":
            # Autism mode: preserve almost all context to explain idioms
            min_out_len = int(raw_sentence_tokens * 0.85)
            len_penalty = 2.0
        else:  # dyslexia or default
            # Dyslexia: preserve meaning but allow some word removal
            min_out_len = int(raw_sentence_tokens * 0.7)
            len_penalty = 1.5

        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=128,
                min_length=min_out_len,  # <-- Prevents aggressive deletion
                num_beams=4,
                length_penalty=len_penalty,  # <-- Forces different paths per profile
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                early_stopping=True
            )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Capitalize first letter of each sentence for proper post-processing
        if result:
            result = result[0].upper() + result[1:] if len(result) > 0 else result
            import re
            result = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), result)

        simplified_sentences.append(result.strip())

    return " ".join(simplified_sentences)


def process_text(text: str, mode: str, model_name: str = "./t5", use_hyphenation: bool = False) -> str:
    """Process text according to the specified mode."""
    # 1. Neural Simplification (Shared) - now mode-aware
    simplified = simplify_with_t5(text, model_name, mode=mode)

    # 2. Mode-Specific Post-Processing
    if mode == "dyslexia":
        return format_for_dyslexia(simplified, split_sentences, use_hyphenation)
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
    parser.add_argument(
        "--use-hyphenation",
        action="store_true",
        help="Enable hyphenation of long words (not recommended for dyslexia per BDA guidelines)"
    )

    args = parser.parse_args()

    text = read_input_file(args.input)

    # Select appropriate model
    model_name = _select_model(args.model, text)

    result = process_text(text, args.mode, model_name, args.use_hyphenation)
    print(result)

    if args.metrics:
        metrics = compute_metrics(text, result)
        print_metrics(metrics)


if __name__ == "__main__":
    main()
