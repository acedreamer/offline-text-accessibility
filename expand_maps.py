#!/usr/bin/env python3
"""
Expand idiom and jargon maps by generating morphological variants.
For each phrase, generate 4-5 variants (verb tenses, conjugations, forms)
to increase coverage and make the library more comprehensive.
"""

import json
import re
from typing import Dict, List, Set
from pathlib import Path

def load_json(path: str) -> Dict:
    """Load JSON file with metadata."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Dict, path: str):
    """Save JSON with pretty formatting."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved {path}")

def is_verb_form(word: str) -> bool:
    """Check if word might be a verb (heuristic)."""
    # English verbs often end in these patterns
    verb_indicators = ['ate', 'ed', 'ing', 'ise', 'ize', 'en', 'ify']
    word_lower = word.lower()
    return any(word_lower.endswith(pattern) for pattern in verb_indicators) or word_lower in ['is', 'am', 'are', 'was', 'were', 'be', 'do', 'does', 'did', 'have', 'has', 'had']

def generate_verb_variants(phrase: str) -> List[str]:
    """
    Generate morphological variants of a phrase containing verbs.
    This handles common English verb transformations.
    """
    words = phrase.split()
    variants = []

    # For single-word idioms
    if len(words) == 1:
        word = words[0].lower()
        variants = generate_single_word_variants(word)
        return [v.capitalize() if words[0][0].isupper() else v for v in variants]

    # For multi-word idioms, try to transform verbs within
    # Simple heuristics: identify words that might be verbs and generate variants
    for i, word in enumerate(words):
        if is_verb_form(word):
            # Generate variants by changing this word's form
            word_variants = generate_single_word_variants(word.lower())
            for variant in word_variants:
                new_words = words.copy()
                # Preserve capitalization
                if word[0].isupper():
                    variant = variant.capitalize()
                new_words[i] = variant
                variants.append(' '.join(new_words))

    return list(set(variants))  # Deduplicate

def generate_single_word_variants(word: str) -> List[str]:
    """
    Generate morphological variants for a single English word.
    Returns a list including base form and common inflections.
    """
    variants = set([word])  # Always include original

    word_lower = word.lower()

    # Handle common patterns
    if word_lower.endswith('y') and len(word_lower) > 1 and word_lower[-2] not in 'aeiou':
        # Words ending in consonant+y → ies
        if word_lower not in ['play', 'say', 'may', 'day']:  # exceptions
            variants.add(word_lower[:-1] + 'ies')
            variants.add(word_lower[:-1] + 'ied')
    elif word_lower.endswith('e'):
        # Words ending in e → ed, es, ing (often drop e)
        base = word_lower[:-1] if word_lower not in ['be', 'see', 'flee'] else word_lower
        variants.add(base + 'd')  # e.g., "write" → "wrote" (irregular) but "hope" → "hoped"
        variants.add(base + 's')
        variants.add(base + 'ing')
        # Also keep with e
        variants.add(word_lower + 'd')
        variants.add(word_lower + 's')
        variants.add(word_lower + 'ing')
    else:
        # Regular verbs: add s, ed, ing
        variants.add(word_lower + 's')
        variants.add(word_lower + 'ed')
        variants.add(word_lower + 'ing')

    # Add third person singular
    if word_lower.endswith('s') and not word_lower.endswith('ss'):
        variants.add(word_lower + 'es')
    else:
        variants.add(word_lower + 's')

    # Irregular verb patterns (common ones)
    irregular_map = {
        'write': ['wrote', 'written', 'writing', 'writes'],
        'go': ['went', 'gone', 'going', 'goes'],
        'take': ['took', 'taken', 'taking', 'takes'],
        'come': ['came', 'coming', 'comes'],
        'see': ['saw', 'seen', 'seeing', 'sees'],
        'do': ['did', 'done', 'doing', 'does'],
        'get': ['got', 'gotten', 'getting', 'gets'],
        'give': ['gave', 'given', 'giving', 'gives'],
        'find': ['found', 'finding', 'finds'],
        'think': ['thought', 'thinking', 'thinks'],
        'know': ['knew', 'known', 'knowing', 'knows'],
        'break': ['broke', 'broken', 'breaking', 'breaks'],
        'choose': ['chose', 'chosen', 'choosing', 'chooses'],
        'make': ['made', 'making', 'makes'],
        'say': ['said', 'saying', 'says'],
        'pay': ['paid', 'paying', 'pays'],
        'lay': ['laid', 'laying', 'lays'],
        'lie': ['lay', 'lain', 'lying', 'lies'],
        'drive': ['drove', 'driven', 'driving', 'drives'],
        'write': ['wrote', 'written', 'writing', 'writes'],
        'fall': ['fell', 'fallen', 'falling', 'falls'],
        'speak': ['spoke', 'spoken', 'speaking', 'speaks'],
        'begin': ['began', 'begun', 'beginning', 'begins'],
        'drink': ['drank', 'drunk', 'drinking', 'drinks'],
        'eat': ['ate', 'eaten', 'eating', 'eats'],
        'run': ['ran', 'run', 'running', 'runs'],
        'sing': ['sang', 'sung', 'singing', 'sings'],
        'swim': ['swam', 'swum', 'swimming', 'swims'],
        'throw': ['threw', 'thrown', 'throwing', 'throws'],
        'wear': ['wore', 'worn', 'wearing', 'wears'],
    }

    if word_lower in irregular_map:
        variants.update(irregular_map[word_lower])

    # Add gerund/participle forms if not already present
    if word_lower.endswith('e'):
        variants.add(word_lower[:-1] + 'ing')  # e.g., "take" → "taking"
    else:
        variants.add(word_lower + 'ing')

    return list(variants)

def generate_variants_for_phrase(phrase: str, max_variants: int = 5) -> List[str]:
    """
    Generate up to max_variants morphological variants for a phrase.
    Includes the original phrase in the result.
    """
    original = phrase
    variants = generate_verb_variants(phrase)

    # Filter out the original and limit count
    filtered = [v for v in variants if v.lower() != original.lower() and v != original]
    filtered = list(dict.fromkeys(filtered))  # Preserve order, dedupe

    # Return original + up to max_variants-1 new variants
    return [original] + filtered[:max_variants-1]

def expand_dictionary(data: Dict, max_variants: int = 5) -> Dict:
    """
    Expand a dictionary by creating morphological variants of keys.
    Maintains all original entries and adds variants with same value.
    """
    original_metadata = data.get('__metadata__', {})
    original_count = original_metadata.get('count', len(data) - (1 if '__metadata__' in data else 0))

    new_data = {'__metadata__': original_metadata.copy()}
    new_entries = {}

    # Get original entries (exclude metadata)
    original_entries = {k: v for k, v in data.items() if k != '__metadata__'}

    print(f"Processing {len(original_entries)} original entries...")

    for idx, (phrase, meaning) in enumerate(original_entries.items(), 1):
        if idx % 100 == 0:
            print(f"  {idx}/{len(original_entries)} processed...")

        # Generate variants
        variants = generate_variants_for_phrase(phrase, max_variants)

        # Add each variant to new entries
        for variant in variants:
            if variant not in original_entries and variant not in new_entries:
                new_entries[variant] = meaning

    # Combine original and new
    expanded = original_entries.copy()
    expanded.update(new_entries)

    # Update metadata
    expanded['__metadata__'] = original_metadata
    expanded['__metadata__']['count'] = len(expanded) - 1  # Exclude metadata
    expanded['__metadata__']['variants_added'] = len(new_entries)
    expanded['__metadata__']['version'] = f"{original_metadata.get('version', '0')}.expanded"

    print(f"\n[*] Original count: {original_count}")
    print(f"[*] New variants added: {len(new_entries)}")
    print(f"[*] Expanded count: {len(expanded) - 1}")
    print(f"[*] Expansion ratio: {(len(expanded) - 1) / original_count:.2f}x")

    return expanded

def main():
    base_dir = Path('docs/ADHD jsons')

    # Process idiom_map.json
    idiom_path = base_dir / 'idiom_map.json'
    print(f"\n[+] Expanding {idiom_path}...")
    idiom_data = load_json(str(idiom_path))
    expanded_idioms = expand_dictionary(idiom_data, max_variants=5)
    save_json(expanded_idioms, str(idiom_path))

    # Process jargon_map.json
    jargon_path = base_dir / 'jargon_map.json'
    print(f"\n[+] Expanding {jargon_path}...")
    jargon_data = load_json(str(jargon_path))
    expanded_jargon = expand_dictionary(jargon_data, max_variants=5)
    save_json(expanded_jargon, str(jargon_path))

    print("\n[+] Expansion complete! Both files have been updated in place.")

if __name__ == '__main__':
    main()
