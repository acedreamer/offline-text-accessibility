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


def _replace_idioms(text: str) -> str:
    """Replace idioms with literal meanings."""
    result = text
    for idiom, literal in IDIOM_MAP.items():
        pattern = rf'\b{re.escape(idiom)}\b'
        result = re.sub(pattern, literal, result, flags=re.IGNORECASE)
    return result


def format_for_autism(text: str) -> str:
    """Format text for autism accessibility.

    Replaces idioms and figurative language with literal meanings.
    """
    return _replace_idioms(text)
