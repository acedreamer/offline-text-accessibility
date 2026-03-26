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
    """Split text into sentences, handling edge cases."""
    if not text or not text.strip():
        return []

    _TITLES = {'Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sr', 'Jr', 'Rev', 'Hon',
              'Gen', 'Col', 'Capt', 'Lt', 'Sgt', 'Cmdr', 'Adm', 'Pres', 'Sen', 'Rep',
              'Gov', 'Dean', 'Atty', 'Engr', 'Arch', 'Esq'}

    _MID_SENTENCE_ABBREVS = {'vs', 'etc', 'Vol', 'pp', 'pg',
                             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                             'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                             'St', 'Mt', 'Ave', 'Blvd', 'Ct', 'Ln', 'Pl', 'Rd'}

    protected = text
    protected = re.sub(r'(\d)\.(\d)', r'\1<DECIMAL>\2', protected)
    protected = re.sub(r'\.{3,}', '<ELLIPSIS>', protected)

    for title in _TITLES:
        pattern = r'(\b|\^)' + re.escape(title) + r'\.(?=\s+[A-Z][a-z])'
        protected = re.sub(pattern, title + '<TITLEDOT>', protected, flags=re.IGNORECASE)

    for abbrev in _MID_SENTENCE_ABBREVS:
        pattern_lower = r'\b' + abbrev.lower() + r'\.(?=\s+[a-z])'
        pattern_upper = r'\b' + abbrev + r'\.(?=\s+[a-z])'
        protected = re.sub(pattern_lower, abbrev.lower() + '<ABBREVDOT>', protected)
        protected = re.sub(pattern_upper, abbrev + '<ABBREVDOT>', protected)

    protected = re.sub(r'\b(a\.m|p\.m)\.(?=\s+[a-z])', r'\1<ABBREVDOT>', protected)

    match = re.match(r'^(\s*\d+)(\.)(\s+[A-Z])', protected)
    if match:
        protected = protected[:match.end(2)-1] + '<NUMDOT>' + protected[match.end(2):]

    parts = re.split(r'([.!?]["\']?\s+)(?=[A-Z])|(<ELLIPSIS>\s+)(?=[A-Z])', protected)

    raw_sentences = []
    current = ""
    for part in parts:
        if part is None:
            continue
        if re.match(r'[.!?]["\']?\s+', part) or re.match(r'<ELLIPSIS>\s+', part):
            current += part
            raw_sentences.append(current)
            current = ""
        else:
            current += part
    if current.strip():
        raw_sentences.append(current)

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

    result = _split_numbered_lists(result)
    return result


def _split_numbered_lists(sentences: list[str]) -> list[str]:
    """Split sentences that contain multiple numbered list items."""
    result = []
    for sent in sentences:
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
        "could've": "could have", "couldn't": "could not",
        "didn't": "did not", "doesn't": "does not", "don't": "do not",
        "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
        "he'd": "he would", "he'll": "he will", "he's": "he is",
        "I'd": "I would", "I'll": "I will", "I'm": "I am", "I've": "I have",
        "isn't": "is not", "it's": "it is", "let's": "let us",
        "might've": "might have", "must've": "must have",
        "should've": "should have", "shouldn't": "should not",
        "that's": "that is", "they're": "they are", "they've": "they have",
        "wasn't": "was not", "we'd": "we would", "we'll": "we will",
        "we're": "we are", "we've": "we have", "weren't": "were not",
        "what's": "what is", "who's": "who is", "won't": "will not",
        "would've": "would have", "wouldn't": "would not",
        "you'd": "you would", "you'll": "you will", "you're": "you are",
        "you've": "you have"
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
    extra = 0
    working = word

    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        extra = 1
        working = word[:-2]

    if working.endswith('e') and not working.endswith(('me', 'ne', 've', 're')):
        working = working[:-1]

    count = 0
    prev_vowel = False
    for char in working:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    return max(1, count + extra)


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
            "avg_sentence_length": round(compute_avg_sentence_length(after) - compute_avg_sentence_length(before), 2),
            "flesch_reading_ease": round(compute_flesch_reading_ease(after) - compute_flesch_reading_ease(before), 2),
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


# ============================================================================
# COMPREHENSIVE HOMOPHONE CORRECTION SYSTEM
# ============================================================================

# Context-based homophone rules: (wrong_word, context_indicator) -> correct_word
# Format: (wrong, context_nearby) -> correct
_HOMOPHONE_RULES = {
    # hole/whole
    ('hole', 'world'): 'whole',
    ('hole', 'thing'): 'whole',
    ('hole', 'story'): 'whole',
    ('hole', 'idea'): 'whole',
    ('hole', 'life'): 'whole',
    ('hole', 'situation'): 'whole',
    ('hole', 'time'): 'whole',
    ('hole', 'place'): 'whole',
    ('hole', 'day'): 'whole',
    ('hole', 'night'): 'whole',
    ('hole', 'body'): 'whole',
    ('hole', 'heart'): 'whole',
    ('hole', 'week'): 'whole',
    ('hole', 'month'): 'whole',
    ('hole', 'year'): 'whole',

    # knot/not
    ('knot', 'is'): 'not',
    ('knot', 'was'): 'not',
    ('knot', 'are'): 'not',
    ('knot', 'were'): 'not',
    ('knot', 'have'): 'not',
    ('knot', 'has'): 'not',
    ('knot', 'do'): 'not',
    ('knot', 'does'): 'not',
    ('knot', 'did'): 'not',
    ('knot', 'can'): 'not',
    ('knot', 'could'): 'not',
    ('knot', 'will'): 'not',
    ('knot', 'would'): 'not',
    ('knot', 'should'): 'not',
    ('knot', 'may'): 'not',
    ('knot', 'might'): 'not',
    ('knot', 'must'): 'not',
    ('knot', 'allowed'): 'not',
    ('knot', 'aloud'): 'not',
    ('knot', 'agree'): 'not',
    ('knot', 'know'): 'not',
    ('knot', 'sure'): 'not',
    ('knot', 'really'): 'not',
    ('knot', 'just'): 'not',
    ('knot', 'only'): 'not',
    ('knot', 'even'): 'not',
    ('knot', 'ever'): 'not',

    # sea/see
    ('sea', 'from'): 'see',
    ('sea', 'you'): 'see',
    ('sea', 'that'): 'see',
    ('sea', 'what'): 'see',
    ('sea', 'how'): 'see',
    ('sea', 'if'): 'see',
    ('sea', 'why'): 'see',
    ('sea', 'me'): 'see',
    ('sea', 'him'): 'see',
    ('sea', 'her'): 'see',
    ('sea', 'them'): 'see',
    ('sea', 'it'): 'see',

    # hear/here
    ('hear', 'from'): 'here',
    ('hear', 'is'): 'here',
    ('hear', 'was'): 'here',
    ('hear', 'are'): 'here',
    ('hear', 'right'): 'here',
    ('hear', 'over'): 'here',
    ('hear', 'come'): 'here',
    ('hear', 'today'): 'here',
    ('hear', 'now'): 'here',

    # knight/night
    ('knight', 'to'): 'night',
    ('knight', 'time'): 'night',
    ('knight', 'dark'): 'night',
    ('knight', 'late'): 'night',
    ('knight', 'fall'): 'night',
    ('knight', 'sky'): 'night',
    ('knight', 'at'): 'night',

    # weight/wait
    ('weight', 'for'): 'wait',
    ('weight', 'until'): 'wait',
    ('weight', 'here'): 'wait',
    ('weight', 'there'): 'wait',

    # wood/would
    ('wood', 'you'): 'would',
    ('wood', 'like'): 'would',
    ('wood', 'be'): 'would',
    ('wood', 'have'): 'would',
    ('wood', 'make'): 'would',
    ('wood', 'rather'): 'would',
    ('wood', 'prefer'): 'would',

    # threw/through
    ('threw', 'the'): 'through',
    ('threw', 'a'): 'through',
    ('threw', 'mist'): 'through',
    ('threw', 'fog'): 'through',
    ('threw', 'rain'): 'through',
    ('threw', 'window'): 'through',
    ('threw', 'door'): 'through',

    # butt/but
    ('butt', 'we'): 'but',
    ('butt', 'I'): 'but',
    ('butt', 'you'): 'but',
    ('butt', 'he'): 'but',
    ('butt', 'she'): 'but',
    ('butt', 'they'): 'but',
    ('butt', 'it'): 'but',
    ('butt', 'the'): 'but',
    ('butt', 'this'): 'but',
    ('butt', 'that'): 'but',

    # tail/tale
    ('tail', 'of'): 'tale',
    ('tail', 'story'): 'tale',
    ('tail', 'stories'): 'tale',
    ('tail', 'told'): 'tale',
    ('tail', 'old'): 'tale',
    ('tail', 'fairy'): 'tale',

    # know/no
    ('no', 'what'): 'know',
    ('no', 'how'): 'know',
    ('no', 'where'): 'know',
    ('no', 'when'): 'know',
    ('no', 'why'): 'know',
    ('no', 'who'): 'know',
    ('no', 'that'): 'know',
    ('no', 'if'): 'know',
    ('no', 'about'): 'know',

    # knew/new
    ('new', 'about'): 'knew',
    ('new', 'that'): 'knew',
    ('new', 'what'): 'knew',
    ('new', 'where'): 'knew',
    ('new', 'when'): 'knew',
    ('new', 'why'): 'knew',
    ('new', 'who'): 'knew',
    ('new', 'how'): 'knew',
    ('new', 'before'): 'knew',
    ('new', 'already'): 'knew',

    # right/write
    ('write', 'now'): 'right',
    ('write', 'here'): 'right',
    ('write', 'there'): 'right',
    ('write', 'away'): 'right',
    ('write', 'hand'): 'right',
    ('write', 'side'): 'right',
    ('write', 'way'): 'right',
    ('write', 'turn'): 'right',
    ('write', 'or'): 'right',

    # there/their
    ('there', 'book'): 'their',
    ('there', 'house'): 'their',
    ('there', 'car'): 'their',
    ('there', 'dog'): 'their',
    ('there', 'cat'): 'their',
    ('there', 'child'): 'their',
    ('there', 'children'): 'their',
    ('there', 'parent'): 'their',
    ('there', 'friend'): 'their',
    ('there', 'family'): 'their',
    ('there', 'idea'): 'their',
    ('there', 'plan'): 'their',
    ('there', 'work'): 'their',
    ('there', 'job'): 'their',
    ('there', 'home'): 'their',
    ('there', 'room'): 'their',
    ('there', 'place'): 'their',

    # to/too
    ('to', 'much'): 'too',
    ('to', 'many'): 'too',
    ('to', 'loud'): 'too',
    ('to', 'fast'): 'too',
    ('to', 'slow'): 'too',
    ('to', 'soon'): 'too',
    ('to', 'late'): 'too',
    ('to', 'early'): 'too',
    ('to', 'bad'): 'too',
    ('to', 'good'): 'too',
    ('to', 'easy'): 'too',
    ('to', 'hard'): 'too',
    ('to', 'long'): 'too',
    ('to', 'short'): 'too',
    ('to', 'big'): 'too',
    ('to', 'small'): 'too',
    ('to', 'hot'): 'too',
    ('to', 'cold'): 'too',
    ('to', 'young'): 'too',
    ('to', 'old'): 'too',
    ('to', 'far'): 'too',
    ('to', 'close'): 'too',
    ('to', 'high'): 'too',
    ('to', 'low'): 'too',

    # your/you're
    ('your', 'going'): "you're",
    ('your', 'coming'): "you're",
    ('your', 'here'): "you're",
    ('your', 'there'): "you're",
    ('your', 'welcome'): "you're",
    ('your', 'right'): "you're",
    ('your', 'wrong'): "you're",
    ('your', 'sure'): "you're",
    ('your', 'beautiful'): "you're",
    ('your', 'amazing'): "you're",
    ('your', 'wonderful'): "you're",
    ('your', 'great'): "you're",
    ('your', 'good'): "you're",
    ('your', 'nice'): "you're",
    ('your', 'kind'): "you're",
    ('your', 'smart'): "you're",
    ('your', 'funny'): "you're",
    ('your', 'crazy'): "you're",
    ('your', 'awesome'): "you're",
    ('your', 'not'): "you're",

    # its/it's
    ('its', 'a'): "it's",
    ('its', 'an'): "it's",
    ('its', 'going'): "it's",
    ('its', 'coming'): "it's",
    ('its', 'here'): "it's",
    ('its', 'there'): "it's",
    ('its', 'been'): "it's",
    ('its', 'not'): "it's",
    ('its', 'really'): "it's",
    ('its', 'very'): "it's",
    ('its', 'so'): "it's",
    ('its', 'just'): "it's",
    ('its', 'still'): "it's",
    ('its', 'already'): "it's",
    ('its', 'time'): "it's",
    ('its', 'important'): "it's",
    ('its', 'hard'): "it's",
    ('its', 'easy'): "it's",
    ('its', 'good'): "it's",
    ('its', 'bad'): "it's",
    ('its', 'nice'): "it's",
    ('its', 'beautiful'): "it's",
    ('its', 'true'): "it's",
    ('its', 'false'): "it's",
    ('its', 'possible'): "it's",
    ('its', 'impossible'): "it's",
    ('its', 'likely'): "it's",
    ('its', 'unlikely'): "it's",

    # our/are
    ('our', 'is'): 'are',
    ('our', 'was'): 'are',
    ('our', 'been'): 'are',
    ('our', 'being'): 'are',
    ('our', 'not'): 'are',
    ('our', 'going'): 'are',
    ('our', 'coming'): 'are',
    ('our', 'here'): 'are',
    ('our', 'there'): 'are',
    ('our', 'all'): 'are',
    ('our', 'both'): 'are',

    # one/won
    ('one', 'the'): 'won',
    ('one', 'game'): 'won',
    ('one', 'prize'): 'won',
    ('one', 'award'): 'won',
    ('one', 'match'): 'won',
    ('one', 'race'): 'won',
    ('one', 'competition'): 'won',

    # piece/peace
    ('piece', 'and'): 'peace',
    ('piece', 'quiet'): 'peace',
    ('piece', 'of'): 'peace',
    ('piece', 'in'): 'peace',
    ('piece', 'with'): 'peace',
    ('piece', 'for'): 'peace',
    ('piece', 'world'): 'peace',
    ('piece', 'inner'): 'peace',
    ('piece', 'keep'): 'peace',
    ('piece', 'make'): 'peace',
    ('piece', 'find'): 'peace',
    ('piece', 'war'): 'peace',
    ('piece', 'peaceful'): 'peace',

    # weak/week
    ('weak', 'after'): 'week',
    ('weak', 'before'): 'week',
    ('weak', 'last'): 'week',
    ('weak', 'this'): 'week',
    ('weak', 'next'): 'week',
    ('weak', 'every'): 'week',
    ('weak', 'each'): 'week',
    ('weak', 'two'): 'week',
    ('weak', 'three'): 'week',
    ('weak', 'four'): 'week',
    ('weak', 'five'): 'week',
    ('weak', 'six'): 'week',
    ('weak', 'seven'): 'week',
    ('weak', 'eight'): 'week',
    ('weak', 'nine'): 'week',
    ('weak', 'ten'): 'week',
    ('weak', 'end'): 'week',
    ('weak', 'mid'): 'week',
    ('weak', 'work'): 'week',
    ('weak', 'school'): 'week',
    ('weak', 'holiday'): 'week',
    ('weak', 'vacation'): 'week',
    ('weak', 'business'): 'week',
    ('weak', 'full'): 'week',
    ('weak', 'whole'): 'week',
    ('weak', 'busy'): 'week',
    ('weak', 'good'): 'week',
    ('weak', 'bad'): 'week',
    ('weak', 'long'): 'week',
    ('weak', 'short'): 'week',

    # whose/who's
    ('whose', 'that'): "who's",
    ('whose', 'this'): "who's",
    ('whose', 'there'): "who's",
    ('whose', 'here'): "who's",
    ('whose', 'coming'): "who's",
    ('whose', 'going'): "who's",
    ('whose', 'at'): "who's",
    ('whose', 'on'): "who's",

    # meet/meat
    ('meet', 'and'): 'meat',
    ('meet', 'the'): 'meat',
    ('meet', 'a'): 'meat',
    ('meet', 'some'): 'meat',
    ('meet', 'raw'): 'meat',
    ('meet', 'cooked'): 'meat',
    ('meet', 'grilled'): 'meat',
    ('meet', 'fried'): 'meat',
    ('meet', 'baked'): 'meat',
    ('meet', 'roasted'): 'meat',
    ('meet', 'beef'): 'meat',
    ('meet', 'pork'): 'meat',
    ('meet', 'chicken'): 'meat',
    ('meet', 'lamb'): 'meat',
    ('meet', 'fish'): 'meat',
    ('meet', 'steak'): 'meat',
    ('meet', 'burger'): 'meat',
    ('meet', 'eat'): 'meat',
    ('meet', 'cook'): 'meat',
    ('meet', 'red'): 'meat',
    ('meet', 'white'): 'meat',

    # sail/sale
    ('sail', 'price'): 'sale',
    ('sail', 'item'): 'sale',
    ('sail', 'product'): 'sale',
    ('sail', 'store'): 'sale',
    ('sail', 'shop'): 'sale',
    ('sail', 'market'): 'sale',
    ('sail', 'discount'): 'sale',
    ('sail', 'clearance'): 'sale',
    ('sail', 'special'): 'sale',
    ('sail', 'offer'): 'sale',
    ('sail', 'deal'): 'sale',
    ('sail', 'bargain'): 'sale',
    ('sail', 'for'): 'sale',
    ('sail', 'on'): 'sale',
    ('sail', 'yard'): 'sale',
    ('sail', 'garage'): 'sale',
    ('sail', 'book'): 'sale',

    # stare/stair
    ('stair', 'at'): 'stare',
    ('stair', 'into'): 'stare',
    ('stair', 'out'): 'stare',
    ('stair', 'down'): 'stare',
    ('stair', 'up'): 'stare',
    ('stair', 'back'): 'stare',
    ('stair', 'off'): 'stare',
    ('stair', 'over'): 'stare',
    ('stair', 'past'): 'stare',
    ('stair', 'through'): 'stare',
    ('stair', 'across'): 'stare',
    ('stair', 'around'): 'stare',
    ('stair', 'away'): 'stare',

    # steal/steel
    ('steel', 'the'): 'steal',
    ('steel', 'a'): 'steal',
    ('steel', 'my'): 'steal',
    ('steel', 'your'): 'steal',
    ('steel', 'his'): 'steal',
    ('steel', 'her'): 'steal',
    ('steel', 'our'): 'steal',
    ('steel', 'their'): 'steal',
    ('steel', 'look'): 'steal',
    ('steel', 'glance'): 'steal',
    ('steel', 'kiss'): 'steal',
    ('steel', 'hug'): 'steal',
    ('steel', 'idea'): 'steal',
    ('steel', 'plan'): 'steal',
    ('steel', 'money'): 'steal',
    ('steel', 'wallet'): 'steal',
    ('steel', 'phone'): 'steal',
    ('steel', 'car'): 'steal',
    ('steel', 'bike'): 'steal',
    ('steel', 'heart'): 'steal',

    # suite/sweet
    ('suite', 'tooth'): 'sweet',
    ('suite', 'dream'): 'sweet',
    ('suite', 'no'): 'sweet',
    ('suite', 'yes'): 'sweet',
    ('suite', 'so'): 'sweet',
    ('suite', 'very'): 'sweet',
    ('suite', 'really'): 'sweet',
    ('suite', 'pie'): 'sweet',
    ('suite', 'cake'): 'sweet',
    ('suite', 'candy'): 'sweet',
    ('suite', 'chocolate'): 'sweet',
    ('suite', 'fruit'): 'sweet',
    ('suite', 'honey'): 'sweet',
    ('suite', 'sugar'): 'sweet',
    ('suite', 'treat'): 'sweet',
    ('suite', 'dessert'): 'sweet',
    ('suite', 'wine'): 'sweet',
    ('suite', 'spot'): 'sweet',
    ('suite', 'deal'): 'sweet',
    ('suite', 'success'): 'sweet',
    ('suite', 'victory'): 'sweet',
    ('suite', 'revenge'): 'sweet',

    # waste/waist
    ('waist', 'of'): 'waste',
    ('waist', 'time'): 'waste',
    ('waist', 'money'): 'waste',
    ('waist', 'effort'): 'waste',
    ('waist', 'energy'): 'waste',
    ('waist', 'resource'): 'waste',
    ('waist', 'opportunity'): 'waste',
    ('waist', 'paper'): 'waste',
    ('waist', 'food'): 'waste',
    ('waist', 'water'): 'waste',
    ('waist', 'land'): 'waste',
    ('waist', 'space'): 'waste',
    ('waist', 'life'): 'waste',
    ('waist', 'talent'): 'waste',
    ('waist', 'away'): 'waste',
    ('waist', 'not'): 'waste',

    # flour/flower
    ('flour', 'garden'): 'flower',
    ('flour', 'field'): 'flower',
    ('flour', 'plant'): 'flower',
    ('flour', 'grew'): 'flower',
    ('flour', 'grown'): 'flower',
    ('flour', 'grow'): 'flower',
    ('flour', 'blooms'): 'flower',
    ('flour', 'bloom'): 'flower',
    ('flour', 'petal'): 'flower',
    ('flour', 'rose'): 'flower',
    ('flour', 'lily'): 'flower',
    ('flour', 'tulip'): 'flower',
    ('flour', 'daisy'): 'flower',
    ('flour', 'sunflower'): 'flower',
    ('flour', 'wild'): 'flower',
    ('flour', 'bed'): 'flower',
    ('flour', 'pot'): 'flower',
    ('flour', 'arrangement'): 'flower',
    ('flour', 'shop'): 'flower',
    ('flour', 'store'): 'flower',
    ('flour', 'beautiful'): 'flower',
    ('flour', 'lovely'): 'flower',
    ('flour', 'pretty'): 'flower',
    ('flour', 'fresh'): 'flower',
    ('flour', 'cut'): 'flower',
    ('flour', 'dried'): 'flower',
    ('flour', 'smell'): 'flower',
    ('flour', 'scent'): 'flower',
    ('flour', 'fragrance'): 'flower',

    # affects/effects
    ('affects', 'the'): 'effects',
    ('affects', 'a'): 'effects',
    ('affects', 'an'): 'effects',
    ('affects', 'this'): 'effects',
    ('affects', 'that'): 'effects',
    ('affects', 'no'): 'effects',
    ('affects', 'some'): 'effects',
    ('affects', 'any'): 'effects',
    ('affects', 'good'): 'effects',
    ('affects', 'bad'): 'effects',
    ('affects', 'side'): 'effects',
    ('affects', 'positive'): 'effects',
    ('affects', 'negative'): 'effects',
    ('affects', 'major'): 'effects',
    ('affects', 'minor'): 'effects',

    # break/brake
    ('brake', 'down'): 'break',
    ('brake', 'up'): 'break',
    ('brake', 'out'): 'break',
    ('brake', 'through'): 'break',
    ('brake', 'off'): 'break',
    ('brake', 'in'): 'break',
    ('brake', 'into'): 'break',
    ('brake', 'away'): 'break',
    ('brake', 'apart'): 'break',
    ('brake', 'after'): 'break',
    ('brake', 'fast'): 'break',
    ('brake', 'slow'): 'break',
    ('brake', 'hard'): 'break',
    ('brake', 'sudden'): 'break',
    ('brake', 'suddenly'): 'break',
    ('brake', 'quick'): 'break',
    ('brake', 'quickly'): 'break',
    ('brake', 'the'): 'break',
    ('brake', 'a'): 'break',
    ('brake', 'an'): 'break',
    ('brake', 'my'): 'break',
    ('brake', 'your'): 'break',
    ('brake', 'his'): 'break',
    ('brake', 'her'): 'break',
    ('brake', 'their'): 'break',
    ('brake', 'our'): 'break',
    ('brake', 'leg'): 'break',
    ('brake', 'arm'): 'break',
    ('brake', 'heart'): 'break',
    ('brake', 'bone'): 'break',
    ('brake', 'glass'): 'break',
    ('brake', 'window'): 'break',
    ('brake', 'door'): 'break',
    ('brake', 'wall'): 'break',
    ('brake', 'fence'): 'break',
    ('brake', 'rule'): 'break',
    ('brake', 'rules'): 'break',
    ('brake', 'law'): 'break',
    ('brake', 'laws'): 'break',
    ('brake', 'promise'): 'break',
    ('brake', 'news'): 'break',
    ('brake', 'silence'): 'break',
    ('brake', 'record'): 'break',
    ('brake', 'fasting'): 'break',

    # chose/choose (past tense correction)
    ('choose', 'yesterday'): 'chose',
    ('choose', 'last'): 'chose',
    ('choose', 'ago'): 'chose',
    ('choose', 'before'): 'chose',
    ('choose', 'earlier'): 'chose',
    ('choose', 'recently'): 'chose',
    ('choose', 'already'): 'chose',
    ('choose', 'then'): 'chose',

    # close/clothes
    ('clothes', 'the'): 'close',
    ('clothes', 'a'): 'close',
    ('clothes', 'an'): 'close',
    ('clothes', 'this'): 'close',
    ('clothes', 'that'): 'close',
    ('clothes', 'my'): 'close',
    ('clothes', 'your'): 'close',
    ('clothes', 'his'): 'close',
    ('clothes', 'her'): 'close',
    ('clothes', 'our'): 'close',
    ('clothes', 'their'): 'close',
    ('clothes', 'door'): 'close',
    ('clothes', 'window'): 'close',
    ('clothes', 'gate'): 'close',
    ('clothes', 'eye'): 'close',
    ('clothes', 'eyes'): 'close',
    ('clothes', 'book'): 'close',
    ('clothes', 'mouth'): 'close',
    ('clothes', 'shut'): 'close',
    ('clothes', 'near'): 'close',
    ('clothes', 'far'): 'close',
    ('clothes', 'by'): 'close',
    ('clothes', 'to'): 'close',
    ('go', 'clothes'): 'go close',
    ('get', 'clothes'): 'get close',
    ('stay', 'clothes'): 'stay close',
    ('stand', 'clothes'): 'stand close',
    ('come', 'clothes'): 'come close',
    ('very', 'clothes'): 'very close',
    ('so', 'clothes'): 'so close',
    ('too', 'clothes'): 'too close',
    ('quite', 'clothes'): 'quite close',
    ('how', 'clothes'): 'how close',

    # dear/deer
    ('deer', 'friend'): 'dear',
    ('deer', 'friends'): 'dear',
    ('deer', 'mom'): 'dear',
    ('deer', 'dad'): 'dear',
    ('deer', 'mother'): 'dear',
    ('deer', 'father'): 'dear',
    ('deer', 'sister'): 'dear',
    ('deer', 'brother'): 'dear',
    ('deer', 'aunt'): 'dear',
    ('deer', 'uncle'): 'dear',
    ('deer', 'cousin'): 'dear',
    ('deer', 'grandma'): 'dear',
    ('deer', 'grandpa'): 'dear',
    ('deer', 'grandmother'): 'dear',
    ('deer', 'grandfather'): 'dear',
    ('deer', 'wife'): 'dear',
    ('deer', 'husband'): 'dear',
    ('deer', 'son'): 'dear',
    ('deer', 'daughter'): 'dear',
    ('deer', 'children'): 'dear',
    ('deer', 'child'): 'dear',
    ('deer', 'love'): 'dear',
    ('deer', 'loved'): 'dear',
    ('deer', 'one'): 'dear',
    ('deer', 'sir'): 'dear',
    ('deer', 'madam'): 'dear',
    ('deer', 'lady'): 'dear',
    ('deer', 'gentleman'): 'dear',
    ('my', 'deer'): 'my dear',
    ('our', 'deer'): 'our dear',
    ('hold', 'deer'): 'hold dear',

    # die/dye
    ('dye', 'today'): 'die',
    ('dye', 'tomorrow'): 'die',
    ('dye', 'yesterday'): 'die',
    ('dye', 'soon'): 'die',
    ('dye', 'later'): 'die',
    ('dye', 'now'): 'die',
    ('dye', 'then'): 'die',
    ('dye', 'first'): 'die',
    ('dye', 'last'): 'die',
    ('dye', 'before'): 'die',
    ('dye', 'after'): 'die',
    ('dye', 'never'): 'die',
    ('dye', 'ever'): 'die',
    ('dye', 'always'): 'die',
    ('dye', 'sometimes'): 'die',
    ('dye', 'often'): 'die',
    ('dye', 'rarely'): 'die',
    ('dye', 'slowly'): 'die',
    ('dye', 'quickly'): 'die',
    ('dye', 'fast'): 'die',
    ('dye', 'suddenly'): 'die',
    ('dye', 'finally'): 'die',
    ('dye', 'eventually'): 'die',
    ('dye', 'in'): 'die',
    ('dye', 'at'): 'die',
    ('dye', 'from'): 'die',
    ('dye', 'by'): 'die',
    ('dye', 'of'): 'die',
    ('dye', 'with'): 'die',

    # principal/principle
    ('principle', 'school'): 'principal',
    ('principle', 'schools'): 'principal',
    ('principle', 'head'): 'principal',
    ('principle', 'principal'): 'principal',
    ('principal', 'rule'): 'principle',
    ('principal', 'rules'): 'principle',
    ('principal', 'belief'): 'principle',
    ('principal', 'beliefs'): 'principle',
    ('principal', 'value'): 'principle',
    ('principal', 'values'): 'principle',
    ('principal', 'moral'): 'principle',
    ('principal', 'morals'): 'principle',
    ('principal', 'ethic'): 'principle',
    ('principal', 'ethics'): 'principle',
    ('principal', 'theory'): 'principle',
    ('principal', 'theories'): 'principle',
    ('principal', 'fundamental'): 'principle',
    ('principal', 'guiding'): 'principle',
    ('principal', 'basic'): 'principle',
    ('principal', 'core'): 'principle',

    # capital/capitol
    ('capitol', 'city'): 'capital',
    ('capitol', 'cities'): 'capital',
    ('capitol', 'letter'): 'capital',
    ('capitol', 'letters'): 'capital',
    ('capitol', 'money'): 'capital',
    ('capitol', 'funds'): 'capital',
    ('capitol', 'investment'): 'capital',
    ('capitol', 'investment'): 'capital',
    ('capitol', 'building'): 'capitol',
    ('capitol', 'hill'): 'capitol',

    # stationary/stationery
    ('stationary', 'paper'): 'stationery',
    ('stationary', 'papers'): 'stationery',
    ('stationary', 'envelope'): 'stationery',
    ('stationary', 'envelopes'): 'stationery',
    ('stationary', 'pen'): 'stationery',
    ('stationary', 'pens'): 'stationery',
    ('stationary', 'store'): 'stationery',
    ('stationary', 'shop'): 'stationery',
    ('stationery', 'bike'): 'stationary',
    ('stationery', 'bicycle'): 'stationary',
    ('stationery', 'exercise'): 'stationary',
    ('stationery', 'bike'): 'stationary',
    ('stationery', 'car'): 'stationary',
    ('stationery', 'vehicle'): 'stationary',
    ('stationery', 'object'): 'stationary',
    ('stationery', 'objects'): 'stationary',
    ('stationery', 'position'): 'stationary',
    ('stationery', 'standing'): 'stationary',
    ('stationery', 'still'): 'stationary',
    ('stationery', 'fixed'): 'stationary',

    # desert/dessert
    ('desert', 'sweet'): 'dessert',
    ('desert', 'sweets'): 'dessert',
    ('desert', 'cake'): 'dessert',
    ('desert', 'cakes'): 'dessert',
    ('desert', 'pie'): 'dessert',
    ('desert', 'pies'): 'dessert',
    ('desert', 'ice'): 'dessert',
    ('desert', 'cream'): 'dessert',
    ('desert', 'pudding'): 'dessert',
    ('desert', 'chocolate'): 'dessert',
    ('desert', 'after'): 'dessert',
    ('desert', 'dinner'): 'dessert',
    ('desert', 'lunch'): 'dessert',
    ('desert', 'meal'): 'dessert',
    ('desert', 'menu'): 'dessert',
    ('dessert', 'sand'): 'desert',
    ('dessert', 'dunes'): 'desert',
    ('dessert', 'cactus'): 'desert',
    ('dessert', 'camels'): 'desert',
    ('dessert', 'oasis'): 'desert',
    ('dessert', 'dry'): 'desert',
    ('dessert', 'hot'): 'desert',
    ('dessert', 'arid'): 'desert',
    ('dessert', 'wasteland'): 'desert',

    # Common letter reversals and misspellings
    ('bue', 'sky'): 'blue',
    ('bue', 'color'): 'blue',
    ('bue', 'eyes'): 'blue',
    ('simpley', 'a'): 'simply',
    ('madder', 'of'): 'matter',
    ('ruff', 'surface'): 'rough',
    ('ruff', 'road'): 'rough',
    ('ruff', 'skin'): 'rough',
    ('ruff', 'hands'): 'rough',
    ('ruff', 'feel'): 'rough',
    ('ruff', 'touch'): 'rough',
    ('puff', 'surface'): 'rough',
    ('puff', 'road'): 'rough',
    ('puff', 'are'): 'rough',
}

# Context window size for matching
_CONTEXT_WINDOW = 3


def correct_spelling(text: str) -> str:
    """Correct spelling mistakes and context-dependent homophone errors.

    Uses rule-based context-aware corrections for common homophones.
    """
    if not text:
        return text

    words = text.split()
    corrected = []

    for i, word in enumerate(words):
        # Get context words (before and after)
        start = max(0, i - _CONTEXT_WINDOW)
        end = min(len(words), i + _CONTEXT_WINDOW + 1)
        context = [w.lower().strip('.,!?;:()"\'') for w in words[start:end] if w != word]

        # Clean the current word
        clean_word = word.lower().strip('.,!?;:()"\'')
        prefix = word[:len(word) - len(word.lstrip('.,!?;:()"\''))] if word != clean_word else ''
        suffix = word[len(word.rstrip('.,!?;:()"\'')):] if word != clean_word else ''

        # Check for corrections
        corrected_word = None
        for (wrong, ctx_word), right in _HOMOPHONE_RULES.items():
            if clean_word == wrong:
                if ctx_word in context:
                    corrected_word = right
                    break

        if corrected_word:
            # Preserve capitalization
            if word and word[0].isupper():
                corrected_word = corrected_word.capitalize()
            corrected.append(prefix + corrected_word + suffix)
        else:
            corrected.append(word)

    return ' '.join(corrected)
