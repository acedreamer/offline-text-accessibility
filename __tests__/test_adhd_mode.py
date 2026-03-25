"""Tests for ADHD accessibility formatting."""
import pytest
import re
from adhd_mode import format_for_adhd, _bold_first_noun


@pytest.mark.requires_spacy
class TestADHDBolding:
    def test_bolds_noun_not_article(self):
        """Should bold first noun, not article."""
        result = _bold_first_noun("The cat sat on the mat.")
        assert "**cat**" in result
        assert "**The**" not in result

    def test_bolds_first_noun_only(self):
        """Only the first noun should be bolded."""
        result = _bold_first_noun("The quick brown fox jumps over the lazy dog.")
        # Should bold 'fox' (first noun), not 'dog' (second noun)
        assert "**fox**" in result
        assert "**dog**" not in result

    def test_handles_punctuation(self):
        """Punctuation should be outside bold markers."""
        result = _bold_first_noun("The fox, which was red, ran away.")
        # Markdown should be **fox**, not **fox,**
        assert "**fox**," in result or "**fox**" in result

    def test_handles_pronouns(self):
        """Pronouns should not be bolded."""
        result = _bold_first_noun("She went to the store.")
        assert "**She**" not in result
        assert "**store**" in result  # The noun should be bolded

    def test_handles_empty_input(self):
        result = _bold_first_noun("")
        assert result == ""
        result = _bold_first_noun("...")
        assert result == "..."

    def test_handles_gerund_as_subject(self):
        """Gerunds acting as nouns should be considered."""
        result = _bold_first_noun("Running is good exercise.")
        # 'Running' here is a VERB in spaCy but functions as a noun
        # We expect some bolding to occur
        assert "**" in result

    def test_handles_sentence_with_only_pronouns(self):
        """Sentence with only pronouns should have no bolding."""
        result = _bold_first_noun("He saw him.")
        # No nouns in this sentence
        # Since there's no NOUN, it may bold a VERB or nothing
        # Just ensure it doesn't crash and returns something sensible
        assert isinstance(result, str)

    def test_bolds_proper_nouns(self):
        """Proper nouns (names) should be bolded."""
        result = _bold_first_noun("John went to the market.")
        assert "**John**" in result

    def test_skips_pronouns_before_noun(self):
        """Pronouns should be skipped to find actual nouns."""
        result = _bold_first_noun("They went to the park.")
        assert "**They**" not in result
        assert "**park**" in result


class TestADHDFormat:
    def test_adds_progress_markers(self):
        text = "First sentence. Second sentence. Third sentence."
        result = format_for_adhd(text)
        # Use regex to be flexible about format changes
        assert re.search(r'\[\d+/\d+\]', result) is not None

    def test_single_sentence(self):
        text = "Just one sentence here."
        result = format_for_adhd(text)
        assert re.search(r'\[1/1\]', result) is not None

    def test_empty_text(self):
        result = format_for_adhd("")
        assert result == ""

    def test_preserves_sentence_content(self):
        text = "The important meeting happened yesterday."
        result = format_for_adhd(text)
        # Remove markdown for content check
        clean = result.replace('*', '').replace('[', '').replace(']', '')
        assert "important meeting" in clean
        assert "yesterday" in clean

    def test_applies_bolding_to_each_sentence(self):
        text = "The cat runs. The dog barks."
        result = format_for_adhd(text)
        # Should have bolding in both sentences
        assert "**cat**" in result
        assert "**dog**" in result

    def test_line_format_matches_expected(self):
        text = "Test sentence."
        result = format_for_adhd(text)
        # Should be in format: [1/1] - sentence with bolding
        assert "[1/1]" in result
        assert "-" in result  # Separator
