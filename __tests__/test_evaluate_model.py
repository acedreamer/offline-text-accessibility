"""Tests for model evaluation metrics."""
import pytest


class TestMetrics:
    def test_sari_basic(self):
        """SARI compares source, prediction, and references."""
        from evaluate_model import compute_sari
        source = "The magnificent elephant traversed the extensive savanna."
        prediction = "The big elephant walked across the wide savanna."
        references = ["The large elephant crossed the broad savanna."]
        score = compute_sari(source, prediction, references)
        assert 0 <= score <= 100

    def test_bleu_identical(self):
        """BLEU score for identical strings should be high."""
        from evaluate_model import compute_bleu
        prediction = "The cat sat on the mat."
        reference = "The cat sat on the mat."
        score = compute_bleu(reference, prediction)
        assert score == 100.0  # Perfect match

    def test_fkgl_simple_text(self):
        """FKGL returns grade level, not percentage. Simple text = low grade."""
        from evaluate_model import compute_fkgl
        text = "The cat sat. The dog ran."
        score = compute_fkgl(text)
        # FKGL is grade level (0-18ish). Simple text should be < 5
        assert 0 <= score < 5, f"Expected FKGL < 5 for simple text, got {score}"

    def test_fkgl_complex_text(self):
        """Complex text should have higher FKGL."""
        from evaluate_model import compute_fkgl
        text = "Utilizing sophisticated pedagogical methodologies necessitates comprehensive understanding of epistemological frameworks."
        score = compute_fkgl(text)
        # Complex text should have higher grade level
        assert score > 5, f"Expected FKGL > 5 for complex text, got {score}"

    def test_flesch_reading_ease_simple(self):
        """Flesch Reading Ease: 90+ for very simple text."""
        from evaluate_model import compute_flesch_reading_ease
        text = "The cat sat. The dog ran."
        score = compute_flesch_reading_ease(text)
        # FRE uses 0-100 scale where 90+ is very easy
        assert score > 80, f"Expected FRE > 80 for simple text, got {score}"

    def test_flesch_reading_ease_empty(self):
        """Empty text should return 0."""
        from evaluate_model import compute_flesch_reading_ease
        assert compute_flesch_reading_ease("") == 0.0

    def test_fkgl_empty(self):
        """Empty text should return 0."""
        from evaluate_model import compute_fkgl
        assert compute_fkgl("") == 0.0
