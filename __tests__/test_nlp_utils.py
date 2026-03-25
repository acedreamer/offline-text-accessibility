"""Tests for NLP utility functions."""
import pytest
from nlp_utils import get_pos_tags, extract_nouns, get_first_noun, get_first_noun_position, is_spacy_available


@pytest.mark.requires_spacy
class TestPOSTagging:
    def test_basic_noun_detection(self):
        text = "The cat sat on the mat."
        nouns = extract_nouns(text)
        assert "cat" in nouns
        assert "mat" in nouns

    def test_first_noun_simple(self):
        text = "Dogs bark loudly."
        noun = get_first_noun(text)
        assert noun == "Dogs"

    def test_first_noun_with_articles(self):
        text = "The quick brown fox jumps."
        noun = get_first_noun(text)
        assert noun == "fox"

    def test_pronoun_not_selected(self):
        text = "He walked to the store."
        noun = get_first_noun(text)
        assert noun != "He"
        assert noun == "store"  # First actual noun

    def test_empty_text(self):
        assert get_first_noun("") is None
        assert extract_nouns("") == []

    def test_first_noun_position_simple(self):
        text = "The cat sat."
        result = get_first_noun_position(text)
        assert result is not None
        noun, start, end = result
        assert noun == "cat"
        # Position should be after "The " (4 chars)
        assert start == 4
        assert end == 7

    def test_first_noun_position_no_noun(self):
        text = "They run."
        result = get_first_noun_position(text)
        assert result is None

    def test_proper_noun_detected(self):
        text = "John went to Paris."
        nouns = extract_nouns(text)
        # Should include proper nouns
        assert "John" in nouns
        assert "Paris" in nouns

    def test_skip_proper_nouns_flag(self):
        text = "Mary went to the store."
        noun = get_first_noun(text, skip_proper=True)
        # Should skip "Mary" and return "store"
        assert noun == "store"
        assert noun != "Mary"


class TestSpacyAvailability:
    def test_is_spacy_available_true(self):
        # spaCy is installed and model downloaded
        assert is_spacy_available() is True

    def test_get_pos_tags_returns_list_of_tuples(self):
        text = "The cat runs."
        tags = get_pos_tags(text)
        assert isinstance(tags, list)
        assert len(tags) > 0
        assert isinstance(tags[0], tuple)
        assert len(tags[0]) == 2  # (token, tag)
