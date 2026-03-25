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
    """Split text into sentences, handling edge cases.

    Handles:
    - Abbreviations (Dr., Mrs., U.S., etc.)
    - Decimal numbers (3.14)
    - Ellipsis (...)
    - Quoted speech with punctuation
    - Volume citations (Vol. 5, pp. 23)
    - Numbered lists (1. First item.)
    """
    if not text or not text.strip():
        return []

    # Titles that are followed by names (should NOT create sentence breaks)
    _TITLES = {'Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sr', 'Jr', 'Rev', 'Hon',
               'Gen', 'Col', 'Capt', 'Lt', 'Sgt', 'Cmdr', 'Adm', 'Pres', 'Sen', 'Rep',
               'Gov', 'Dean', 'Atty', 'Engr', 'Arch', 'Esq'}

    # Abbreviations that only should NOT split when followed by lowercase
    _MID_SENTENCE_ABBREVS = {'vs', 'etc', 'Vol', 'pp', 'pg',
                             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                             'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                             'St', 'Mt', 'Ave', 'Blvd', 'Ct', 'Ln', 'Pl', 'Rd'}

    protected = text

    # Step 1: Protect decimal numbers
    protected = re.sub(r'(\d)\.(\d)', r'\1<DECIMAL>\2', protected)

    # Step 2: Protect ellipsis
    protected = re.sub(r'\.{3,}', '<ELLIPSIS>', protected)

    # Step 3: Protect title + name patterns
    # Match title followed by Capital+lowercase (a name), including at start of text
    for title in _TITLES:
        # Match at word boundary, with lookahead for space + Capital + lowercase
        pattern = r'(\b|\^)' + re.escape(title) + r'\.(?=\s+[A-Z][a-z])'
        protected = re.sub(pattern, title + '<TITLEDOT>', protected, flags=re.IGNORECASE)

    # Step 4: Protect abbreviations when followed by lowercase
    # Note: Check both uppercase and lowercase abbreviation variants without IGNORECASE flag
    for abbrev in _MID_SENTENCE_ABBREVS:
        # Match abbreviation (case-sensitive) followed by lowercase
        pattern_lower = r'\b' + abbrev.lower() + r'\.(?=\s+[a-z])'
        pattern_upper = r'\b' + abbrev + r'\.(?=\s+[a-z])'
        protected = re.sub(pattern_lower, abbrev.lower() + '<ABBREVDOT>', protected)
        protected = re.sub(pattern_upper, abbrev + '<ABBREVDOT>', protected)

    # Step 5: Handle a.m./p.m. - only protect if followed by lowercase
    # Note: Don't use IGNORECASE flag because [a-z] would match uppercase too
    protected = re.sub(r'\b(a\.m|p\.m)\.(?=\s+[a-z])', r'\1<ABBREVDOT>', protected)

    # Step 6: Protect numbered list markers at START only
    # "1. First" at start should stay together
    match = re.match(r'^(\s*\d+)(\.)(\s+[A-Z])', protected)
    if match:
        protected = protected[:match.end(2)-1] + '<NUMDOT>' + protected[match.end(2):]

    # Step 7: Split on sentence boundaries
    # Sentence ends with: punctuation + optional quote + whitespace + Capital letter
    # Use capturing groups to preserve quotes
    parts = re.split(r'([.!?][\"\']?\s+)(?=[A-Z])|(<ELLIPSIS>\s+)(?=[A-Z])', protected)

    # Reconstruct sentences from split parts
    raw_sentences = []
    current = ""
    for part in parts:
        if part is None:
            continue
        if re.match(r'[.!?][\"\']?\s+', part) or re.match(r'<ELLIPSIS>\s+', part):
            # This is a delimiter - add to current and start new
            current += part
            raw_sentences.append(current)
            current = ""
        else:
            current += part
    if current.strip():
        raw_sentences.append(current)

    # Step 8: Restore and filter
    result = []
    for sent in raw_sentences:
        sent = sent.replace('<DECIMAL>', '.')
        sent = sent.replace('<ELLIPSIS>', '...')
        sent = sent.replace('<TITLEDOT>', '.')
        sent = sent.replace('<ABBREVDOT>', '.')
        sent = sent.replace('<NUMDOT>', '.')
        sent = sent.strip()
        if sent:
            result.append(sent)

    # Step 9: Handle numbered lists - split on "N. Capital" patterns
    result = _split_numbered_lists(result)

    return result


def _split_numbered_lists(sentences: list[str]) -> list[str]:
    """Split sentences that contain multiple numbered list items."""
    result = []
    for sent in sentences:
        # Split on "number. Capital" patterns, but not at start
        parts = re.split(r'(?<=[^.])\s+(?=\d+\.\s+[A-Z])', sent)
        if len(parts) > 1:
            for part in parts:
                part = part.strip()
                if part:
                    result.append(part)
        else:
            result.append(sent)
    return result


def get_words(text: str) -> list[str]:
    """Extract words from text, handling hyphenated compounds and contractions."""
    contractions = {
        "ain't": "am not", "aren't": "are not", "can't": "cannot",
        "can't've": "cannot have", "'cause": "because", "could've": "could have",
        "couldn't": "could not", "couldn't've": "could not have", "didn't": "did not",
        "doesn't": "does not", "don't": "do not", "hadn't": "had not",
        "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not",
        "he'd": "he would", "he'd've": "he would have", "he'll": "he will",
        "he'll've": "he will have", "he's": "he is", "how'd": "how did",
        "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
        "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
        "I'll've": "I will have", "I'm": "I am", "I've": "I have",
        "isn't": "is not", "it'd": "it would", "it'd've": "it would have",
        "it'll": "it will", "it'll've": "it will have", "it's": "it is",
        "let's": "let us", "ma'am": "madam", "mayn't": "may not",
        "might've": "might have", "mightn't": "might not",
        "mightn't've": "might not have", "must've": "must have",
        "mustn't": "must not", "mustn't've": "must not have",
        "needn't": "need not", "needn't've": "need not have",
        "o'clock": "of the clock", "oughtn't": "ought not",
        "oughtn't've": "ought not have", "shan't": "shall not",
        "sha'n't": "shall not", "shan't've": "shall not have",
        "she'd": "she would", "she'd've": "she would have", "she'll": "she will",
        "she'll've": "she will have", "she's": "she is", "should've": "should have",
        "shouldn't": "should not", "shouldn't've": "should not have",
        "so've": "so have", "so's": "so as", "that'd": "that would",
        "that'd've": "that would have", "that's": "that is",
        "there'd": "there would", "there'd've": "there would have",
        "there's": "there is", "they'd": "they would", "they'd've": "they would have",
        "they'll": "they will", "they'll've": "they will have",
        "they're": "they are", "they've": "they have", "to've": "to have",
        "wasn't": "was not", "we'd": "we would", "we'd've": "we would have",
        "we'll": "we will", "we'll've": "we will have", "we're": "we are",
        "we've": "we have", "weren't": "were not", "what'll": "what will",
        "what'll've": "what will have", "what're": "what are",
        "what's": "what is", "what've": "what have", "when's": "when is",
        "when've": "when have", "where'd": "where did", "where've": "where have",
        "who'll": "who will", "who'll've": "who will have", "who's": "who is",
        "who've": "who have", "why's": "why is", "why've": "why have",
        "will've": "will have", "won't": "will not", "won't've": "will not have",
        "would've": "would have", "wouldn't": "would not",
        "wouldn't've": "would not have", "y'all": "you all",
        "y'all'd": "you all would", "y'all'd've": "you all would have",
        "y'all're": "you all are", "y'all've": "you all have",
        "you'd": "you would", "you'd've": "you would have",
        "you'll": "you will", "you'll've": "you will have",
        "you're": "you are", "you've": "you have"
    }

    expanded_text = text
    for contraction, expansion in contractions.items():
        expanded_text = re.sub(rf'\b{re.escape(contraction)}\b', expansion, expanded_text, flags=re.IGNORECASE)

    words = re.findall(r"\b[a-zA-Z]+(?:[-'][a-zA-Z]+)*\b", expanded_text)
    return words


_SYLLABLE_EXCEPTIONS = {
    'queue': 1, 'gone': 1, 'business': 2, 'people': 2,
    'every': 2, 'different': 3, 'interesting': 4, 'beautiful': 3,
    'family': 3, 'chocolate': 3, 'probably': 3, 'maybe': 2,
    'fire': 2, 'hour': 1, 'our': 1, 'flower': 2,
    'world': 1, 'child': 1, 'children': 2, 'answer': 2,
    'really': 2, 'actually': 4, 'basically': 4,
    'sense': 1, 'dance': 1, 'change': 1, 'please': 1,
    'prose': 1, 'cheese': 1, 'nurse': 1, 'horse': 1,
    'table': 2, 'little': 2, 'able': 2, 'fable': 2,
    'make': 1, 'time': 1, 'home': 1, 'dome': 1,
    'come': 1, 'some': 1, 'love': 1, 'move': 1,
    'hello': 2, 'cable': 2, 'bottle': 2, 'apple': 2,
}


def count_syllables(word: str) -> int:
    """Count syllables in a word using heuristics and exception dictionary."""
    word = word.lower().strip()
    if not word:
        return 0
    word = re.sub(r'[^a-z]', '', word)
    if not word:
        return 0
    if word in _SYLLABLE_EXCEPTIONS:
        return _SYLLABLE_EXCEPTIONS[word]
    if len(word) <= 3:
        return 1

    vowels = 'aeiouy'
    extra_syllable = 0
    working_word = word

    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        extra_syllable = 1
        working_word = word[:-2]

    if working_word.endswith('e') and not working_word.endswith(('me', 'ne', 've', 're')):
        working_word = working_word[:-1]

    count = 0
    prev_is_vowel = False
    for char in working_word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    count += extra_syllable
    return max(1, count)


def compute_avg_sentence_length(text: str) -> float:
    sentences = split_sentences(text)
    if not sentences:
        return 0.0
    words = get_words(text)
    return len(words) / len(sentences)


def compute_flesch_reading_ease(text: str) -> float:
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
    return len(get_words(text))


def compute_metrics(before: str, after: str) -> dict:
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
    print("\n--- Readability Metrics ---")
    print(f"{'Metric':<25} {'Before':>10} {'After':>10} {'Change':>10}")
    print("-" * 57)
    print(f"{'Word count':<25} {metrics['before']['word_count']:>10} {metrics['after']['word_count']:>10} {metrics['change']['word_count']:>+10}")
    print(f"{'Avg sentence length':<25} {metrics['before']['avg_sentence_length']:>10.2f} {metrics['after']['avg_sentence_length']:>10.2f} {metrics['change']['avg_sentence_length']:>+10.2f}")
    print(f"{'Flesch Reading Ease':<25} {metrics['before']['flesch_reading_ease']:>10.2f} {metrics['after']['flesch_reading_ease']:>10.2f} {metrics['change']['flesch_reading_ease']:>+10.2f}")
    print("-" * 57)
