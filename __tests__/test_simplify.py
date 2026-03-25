"""Tests for main simplification logic."""
import pytest
import inspect


class TestT5GenerationParams:
    """Tests for T5 generation parameter validation."""

    def test_beam_search_used(self):
        """Beam search should be used for deterministic output."""
        from simplify import simplify_with_t5
        import inspect

        # Get the source code to verify parameters
        source = inspect.getsource(simplify_with_t5)
        # Should use beam search
        assert "num_beams" in source
        assert "num_beams=4" in source

    def test_no_temperature_with_beam_search(self):
        """Temperature should NOT be used with beam search."""
        from simplify import simplify_with_t5
        import inspect

        source = inspect.getsource(simplify_with_t5)
        # Should NOT have temperature parameter
        assert "temperature" not in source or "temperature=0" not in source
        # Should use early_stopping with beam search
        assert "early_stopping" in source

    def test_length_penalty_positive(self):
        """Length penalty should encourage longer outputs (>= 1.0)."""
        from simplify import simplify_with_t5
        import inspect

        source = inspect.getsource(simplify_with_t5)
        # Should have length_penalty parameter with value >= 1.0
        assert "length_penalty" in source
        assert "1.2" in source or "length_penalty=1.2" in source

    def test_max_length_increased(self):
        """max_length should be increased from 128 to 256."""
        from simplify import simplify_with_t5
        import inspect

        source = inspect.getsource(simplify_with_t5)
        # Should have max_length=256 (not 128)
        assert "max_length=256" in source
        assert "max_length=128" not in source


class TestProcessText:
    """Tests for process_text function interface."""

    def test_process_text_accepts_mode_kwarg(self):
        """process_text should accept mode parameter."""
        from simplify import process_text
        sig = inspect.signature(process_text)
        params = sig.parameters
        assert 'mode' in params

    def test_process_text_accepts_model_name_kwarg(self):
        """process_text should accept model_name parameter."""
        from simplify import process_text
        sig = inspect.signature(process_text)
        params = sig.parameters
        assert 'model_name' in params

    def test_process_text_accepts_use_hyphenation_kwarg(self):
        """process_text should accept use_hyphenation parameter."""
        from simplify import process_text
        sig = inspect.signature(process_text)
        params = sig.parameters
        assert 'use_hyphenation' in params

    def test_process_text_has_correct_defaults(self):
        """process_text should have sensible defaults."""
        from simplify import process_text
        sig = inspect.signature(process_text)
        params = sig.parameters

        # Check default values
        assert params['mode'].default is inspect.Parameter.empty
        assert params['model_name'].default == "t5-small"
        assert params['use_hyphenation'].default is False
