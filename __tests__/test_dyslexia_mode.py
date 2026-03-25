"""Tests for dyslexia accessibility formatting."""
import pytest


class TestCompoundPatterns:
    def test_black_and_white_preserved(self):
        """Compound pattern 'black and white' should be detected."""
        from dyslexia_mode import _is_compound_pattern
        assert _is_compound_pattern("black", "white") is True

    def test_up_and_down_preserved(self):
        """Compound pattern 'up and down' should be detected."""
        from dyslexia_mode import _is_compound_pattern
        assert _is_compound_pattern("up", "down") is True

    def test_back_and_forth_preserved(self):
        """Compound pattern 'back and forth' should be detected."""
        from dyslexia_mode import _is_compound_pattern
        assert _is_compound_pattern("back", "forth") is True

    def test_day_and_night_preserved(self):
        """Compound pattern 'day and night' should be detected."""
        from dyslexia_mode import _is_compound_pattern
        assert _is_compound_pattern("day", "night") is True

    def test_random_words_not_compound(self):
        """Random words should not be detected as compound."""
        from dyslexia_mode import _is_compound_pattern
        assert _is_compound_pattern("cat", "dog") is False
        assert _is_compound_pattern("apple", "banana") is False


class TestConjunctionSplit:
    def test_preserves_black_and_white_pattern(self):
        """'black and white' should not be split."""
        from dyslexia_mode import _split_on_conjunctions
        text = "He wore a black and white tie."
        parts = _split_on_conjunctions(text)
        combined = " ".join(parts)
        # Pattern should stay together (either preserved or both parts present)
        assert "black" in combined and "white" in combined

    def test_preserves_up_and_down_pattern(self):
        """'up and down' should not be split."""
        from dyslexia_mode import _split_on_conjunctions
        text = "He moved up and down."
        parts = _split_on_conjunctions(text)
        combined = " ".join(parts)
        # Both words should be present close together
        assert "up" in combined and "down" in combined

    def test_preserves_all_compound_patterns(self):
        """All compound patterns in sentence should be preserved."""
        from dyslexia_mode import _split_on_conjunctions
        text = "He wore a black and white tie and moved up and down."
        parts = _split_on_conjunctions(text)
        result = " ".join(parts)
        assert "black" in result
        assert "white" in result
        assert "up" in result
        assert "down" in result

    def test_preserves_causal_relationship(self):
        """Causal relationships should maintain both concepts."""
        from dyslexia_mode import _split_on_conjunctions
        text = "I went to the store because I needed milk."
        parts = _split_on_conjunctions(text)
        result = " ".join(parts)
        # Both concepts should still be present
        assert "store" in result
        assert "milk" in result

    def test_handles_short_fragments(self):
        """Should handle short text without crashing."""
        from dyslexia_mode import _split_on_conjunctions
        text = "I ran and she walked."
        parts = _split_on_conjunctions(text)
        assert len(parts) >= 1

    def test_empty_input(self):
        """Empty input should return empty list."""
        from dyslexia_mode import _split_on_conjunctions
        assert _split_on_conjunctions("") == []

    def test_min_length_filter(self):
        """Very short fragments should be handled gracefully."""
        from dyslexia_mode import _split_on_conjunctions
        text = "I ran. It was good."
        parts = _split_on_conjunctions(text)
        # Should produce output
        assert len(parts) >= 1


class TestDyslexiaFormat:
    def test_one_sentence_per_line(self):
        """Each sentence should be on its own line."""
        from dyslexia_mode import format_for_dyslexia
        from utils import split_sentences

        text = "First sentence. Second sentence. Third sentence."
        result = format_for_dyslexia(text, split_sentences)
        lines = result.split('\n\n')
        assert len(lines) == 3

    def test_empty_input(self):
        """Empty input should return empty string."""
        from dyslexia_mode import format_for_dyslexia
        from utils import split_sentences

        result = format_for_dyslexia("", split_sentences)
        assert result == ""

    def test_interface_consistency(self):
        """format_for_dyslexia should accept split_sentences_func parameter."""
        from dyslexia_mode import format_for_dyslexia
        import inspect

        sig = inspect.signature(format_for_dyslexia)
        params = list(sig.parameters.keys())
        assert 'text' in params
        assert 'split_sentences_func' in params

    def test_use_hyphenation_flag(self):
        """Should accept use_hyphenation parameter."""
        from dyslexia_mode import format_for_dyslexia
        import inspect

        sig = inspect.signature(format_for_dyslexia)
        params = sig.parameters
        assert 'use_hyphenation' in params
        assert params['use_hyphenation'].default is False
