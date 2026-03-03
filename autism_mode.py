"""Autism accessibility formatting logic."""
import re

IDIOM_MAP = {
    "piece of cake": "easy",
    "break a leg": "good luck",
    "hit the nail on the head": "exactly correct",
    "under the weather": "feeling sick",
    "cost an arm and a leg": "very expensive",
    "let the cat out of the bag": "revealed a secret",
    "bite the bullet": "endure something difficult",
    "once in a blue moon": "very rarely",
    "break the ice": "start a conversation",
    "spill the beans": "reveal information",
    "ball is in your court": "your decision",
    "see eye to eye": "agree",
    "back to the drawing board": "start over",
    "the whole nine yards": "everything",
    "on the same page": "in agreement",
    "raining cats and dogs": "raining heavily",
    "kick the bucket": "die",
    "beat around the bush": "avoid the main topic",
    "burning the midnight oil": "working late",
    "a penny for your thoughts": "what are you thinking",
}

# Academic/medical terms — replaced literally (case-sensitive, acronyms exact-match)
JARGON_MAP = {
    "volBMD": "bone mineral density",
    "DXA": "bone density scan",
    "CSMI": "cross-sectional moment of inertia",
    "BMC": "bone mineral content",
    "BSI": "bone strength index",
    "MRI": "magnetic resonance imaging",
    "CSA": "cross-sectional area",
    "myocardial infarction": "heart attack",
    "hypertension": "high blood pressure",
    "renal": "kidney-related",
    "hepatic": "liver-related",
    "pulmonary": "lung-related",
    "cognition": "thinking and memory",
    "efficacy": "how well it works",
    "placebo": "inactive dummy treatment",
    "statistically significant": "unlikely to be by chance",
    "et al.": "and others",
    "i.e.": "that is",
    "e.g.": "for example",
}


def _replace_idioms(text: str) -> str:
    """Replace idioms with literal meanings (case-insensitive)."""
    result = text
    for idiom, literal in IDIOM_MAP.items():
        pattern = rf'\b{re.escape(idiom)}\b'
        result = re.sub(pattern, f"**{literal}**", result, flags=re.IGNORECASE)
    return result


def _replace_jargon(text: str) -> str:
    """Replace academic/medical jargon with plain language.

    Acronyms are matched case-sensitively (MRI != mri).
    Multi-word terms are matched case-insensitively.
    """
    result = text
    for term, plain in JARGON_MAP.items():
        if term.isupper() or any(c.isupper() for c in term[1:]):
            # Acronym or mixed-case: exact match, word boundary
            pattern = rf'(?<!\w){re.escape(term)}(?!\w)'
            result = re.sub(pattern, f"**{plain}**", result)
        else:
            # Plain phrase: case-insensitive
            pattern = rf'\b{re.escape(term)}\b'
            result = re.sub(pattern, f"**{plain}**", result, flags=re.IGNORECASE)
    return result


def format_for_autism(text: str) -> str:
    """Format text for autism/literal clarity accessibility.

    Replaces idioms and academic jargon with plain literal language.
    """
    text = _replace_idioms(text)
    text = _replace_jargon(text)
    return text
