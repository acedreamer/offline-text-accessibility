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
    """Split text into sentences, handling common abbreviations and edge cases."""
    # Common abbreviations that shouldn't end sentences
    # Expanded list including more titles, academic, and technical abbreviations
    abbreviations = r'(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|i\.e|e\.g|U\.S|U\.K|p\.m|a\.m|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|St|Mt|Alt|Ave|Blvd|Ct|Dr|Ln|Pl|Rd|Sq|St|Ter|Tr|Way|Ph\.D|M\.D|B\.A|B\.S|M\.A|M\.S|Jr|Sr|Esq|Rev|Hon|Gen|Col|Capt|Lt|Sgt|Cmdr|Adm|Pres|Sen|Rep|Gov|Dean|Prof|Atty|Engr|Arch|RN|MD|DO|DC|DDS|OD|DPM|DVM|PP|PE|PI|CIA|FBI|NASA|NBC|CBS|ABC|CNN|BBC|UN|EU|NATO|OECD|WHO|UNESCO|UNICEF|FIFA|IOC|NBA|NFL|MLB|NHL|MLS|PGA|UFC|WWE|DNA|RNA|HIV|AIDS|GPS|LASER|RADAR|SONAR|ICU|ER|OR|IV|IM|PO|PRN|STAT|bid|tid|qid|qod|hs|ac|pc|ad lib|stat|STAT)'

    # Handle special cases that might interfere with sentence splitting
    # Protect decimal numbers (e.g., 3.14) from being split
    protected_text = re.sub(r'(\d)\.(\d)', r'\1<DECIMAL>\2', text)

    # Protect common patterns like "Vol. 5, pp. 23-45"
    protected_text = re.sub(r'(Vol|vol|pp|pp\.|pg|pg\.)\.\s*(\d+)', r'\1<VOL>\2', protected_text, flags=re.IGNORECASE)

    # Temporarily protect abbreviations by replacing periods with a placeholder
    protected_text = re.sub(rf'\b{abbreviations}\.', lambda m: m.group(0).replace('.', '<PRD>'), protected_text, flags=re.IGNORECASE)

    # Split on sentence endings - handle multiple punctuation marks
    sentences = re.split(r'(?<=[.!?])\s+', protected_text.strip())

    # Restore abbreviations, decimal numbers, and special patterns
    sentences = [s.replace('<PRD>', '.').replace('<DECIMAL>', '.').replace('<VOL>', '.') for s in sentences if s.strip()]

    return sentences

def get_words(text: str) -> list[str]:
    """Extract words from text, handling hyphenated compounds and contractions."""
    # First, handle common contractions by expanding them
    contractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so as",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have"
    }

    # Expand contractions
    expanded_text = text
    for contraction, expansion in contractions.items():
        expanded_text = re.sub(rf'\b{re.escape(contraction)}\b', expansion, expanded_text, flags=re.IGNORECASE)

    # Extract words, preserving hyphenated compounds as single units
    # This pattern matches:
    # - Regular words: [a-zA-Z]+
    # - Hyphenated compounds: [a-zA-Z]+-[a-zA-Z]+ (and potentially more hyphens)
    # - Words with apostrophes that weren't contractions (like possessives): [a-zA-Z]+'[a-zA-Z]+
    words = re.findall(r'\b[a-zA-Z]+(?:[-’\'][a-zA-Z]+)*\b', expanded_text)

    return words

def count_syllables(word: str) -> int:
    """Count syllables in a word using an improved heuristic.

    This implementation handles common English pronunciation rules better
    than the simple vowel group counting approach.
    """
    word = word.lower().strip()
    if not word:
        return 0

    # Remove non-alphabetic characters
    word = re.sub(r'[^a-z]', '', word)

    if len(word) <= 3:
        return 1

    # Remove silent e at end (with exceptions for words ending in le)
    if word.endswith('e') and not word.endswith(('le', 'me')) and len(word) > 3:
        word = word[:-1]

    # Count vowel groups
    vowels = 'aeiouy'
    count = 0
    prev_is_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    # Handle 'le' ending (like "table", "little") - usually adds a syllable
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1

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
