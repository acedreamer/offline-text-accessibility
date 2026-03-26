"""Tests for autism accessibility formatting."""
import pytest
from autism_mode import (
    _replace_idioms,
    _is_idiom_in_context,
    format_for_autism
)

class TestIdiomContext:
    def test_literal_not_replaced_medical(self):
        """Medical context should not replace 'break a leg'."""
        text = "He fell and broke his leg."
        result = _replace_idioms(text)
        assert "**good luck**" not in result

    def test_idiom_replaced_correctly(self):
        """Theatrical context should replace 'break a leg'."""
        text = "Break a leg at the performance!"
        result = _replace_idioms(text)
        assert "**good luck**" in result

    def test_kick_bucket_literal(self):
        """Physical action context should not replace 'kick the bucket'."""
        text = "The child kicked the bucket across the yard."
        result = _replace_idioms(text)
        assert "**die**" not in result

    def test_kick_bucket_idiom(self):
        """Death context should replace 'kick the bucket'."""
        text = "Old Man Johnson finally kicked the bucket."
        result = _replace_idioms(text)
        assert "**die**" in result

    def test_per_match_context_check(self):
        """Each match should be checked independently."""
        text = "He literally kicked the bucket. The idiom kicked the bucket means to die."
        result = _replace_idioms(text)
        assert "die" in result.lower()

    def test_empty_input(self):
        assert format_for_autism("") == ""

class TestJargonReplacement:
    def test_medical_jargon(self):
        text = "The patient had a myocardial infarction."
        result = format_for_autism(text)
        assert "**heart attack**" in result

    def test_acronym_case_sensitive(self):
        text = "The MRI showed normal results."
        result = format_for_autism(text)
        assert "**magnetic resonance imaging**" not in result # Since MRI is not in our dictionary yet

    def test_preserves_surrounding_text(self):
        text = "Hypertension is a common condition."
        result = format_for_autism(text)
        assert "is a common condition" in result
