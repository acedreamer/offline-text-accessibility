"""Automated Test Suite for SimplifyAI NLP Pipeline.

Covers:
- ACCESS Control Token Profiles
- Rule Dictionary Integrity (5,200+ idioms, 2,050+ jargon terms)
- Cognitive Mode Formatters (Dyslexia, ADHD, Autism)
- Deterministic Preprocessing & Homophone / Contraction Normalization
- Readability Telemetry & Syllable / Sentence Metrics
"""
import pytest
import re
from simplify import ACCESS_PROFILES, _select_by_task_complexity
from autism_mode import format_for_autism, _load_idiom_map, _load_jargon_map
from adhd_mode import format_for_adhd
from dyslexia_mode import format_for_dyslexia
from utils import split_sentences, get_words, compute_metrics, correct_spelling


class TestAccessControlTokens:
    """Validate neural generation control tokens for neurodivergent profiles."""

    def test_access_profiles_exist(self):
        expected_keys = {"dyslexia", "adhd", "autism", "default"}
        assert expected_keys.issubset(set(ACCESS_PROFILES.keys()))

    def test_access_token_format(self):
        pattern = re.compile(r"<LengthRatio_\d+> <DepDepth_\d+> <WordRank_\d+> <CCR_\d+>")
        for mode, profile in ACCESS_PROFILES.items():
            assert pattern.match(profile) is not None, f"Invalid token format for {mode}: {profile}"

    def test_adhd_has_aggressive_compression(self):
        # ADHD targets shorter length ratio (LengthRatio_2)
        assert "<LengthRatio_2>" in ACCESS_PROFILES["adhd"]

    def test_autism_preserves_lexical_context(self):
        # Autism mode preserves context to explain figurative terms (LengthRatio_5)
        assert "<LengthRatio_5>" in ACCESS_PROFILES["autism"]


class TestRuleEngineAndDictionaries:
    """Validate 7,200+ entry morphological dictionaries and preprocessing."""

    def test_idiom_dictionary_scale(self):
        idioms = _load_idiom_map()
        assert len(idioms) >= 5000, f"Expected at least 5000 idioms, found {len(idioms)}"

    def test_jargon_dictionary_scale(self):
        jargon = _load_jargon_map()
        assert len(jargon) >= 2000, f"Expected at least 2000 jargon terms, found {len(jargon)}"

    def test_idiom_replacement_accuracy(self):
        sample = "Don't worry, she will kick the bucket soon."
        processed = format_for_autism(sample)
        assert "die" in processed.lower()

    def test_jargon_expansion(self):
        sample = "The patient presented with acute myocardial infarction."
        processed = format_for_autism(sample)
        assert "heart attack" in processed.lower()

    def test_literal_disambiguation_injury(self):
        # A literal break of a leg must not be replaced with 'good luck'
        sample = "The doctor said he broke his leg in the accident."
        processed = format_for_autism(sample)
        assert "good luck" not in processed.lower()

    def test_homophone_correction(self):
        corrected = correct_spelling("He traveled across the hole world.")
        assert "whole" in corrected.lower()


class TestCognitiveModeFormatters:
    """Validate mode-specific cognitive layout transformations."""

    def test_dyslexia_conjunction_splitting(self):
        text = "The quick brown fox jumps over the lazy dog and the bird watched silently."
        formatted = format_for_dyslexia(text, split_sentences_func=split_sentences, use_hyphenation=False)
        lines = [line.strip() for line in formatted.split("\n") if line.strip()]
        assert len(lines) >= 2, "Dyslexia mode should break compound clauses on conjunctions"

    def test_adhd_progress_markers(self):
        text = "First sentence here. Second sentence follows. Third completes it."
        formatted = format_for_adhd(text)
        assert "[1/3]" in formatted
        assert "[2/3]" in formatted
        assert "[3/3]" in formatted

    def test_adhd_noun_bolding(self):
        text = "Elephants remember important trails across the savanna."
        formatted = format_for_adhd(text)
        assert "**" in formatted, "ADHD mode must bold the first salient noun"

    def test_autism_mode_visual_clarity(self):
        text = "It's raining cats and dogs outside."
        formatted = format_for_autism(text)
        assert "**" in formatted, "Replaced idioms must be emphasized for clarity"


class TestReadabilityAndMetrics:
    """Validate sentence splitting, syllable counting, and Flesch telemetry."""

    def test_sentence_splitting_with_abbreviations(self):
        text = "Dr. Smith arrived at 4.50 p.m. He greeted Mr. Jones warmly."
        sentences = split_sentences(text)
        assert len(sentences) == 2, f"Expected 2 sentences, got {len(sentences)}: {sentences}"

    def test_word_extraction_with_contractions(self):
        text = "They didn't believe it couldn't work."
        words = get_words(text)
        assert "did" in words and "not" in words
        assert "could" in words

    def test_compute_metrics_structure(self):
        sample_before = "The incomprehensible manifestations produced overwhelming cognitive perplexity among all observers present."
        sample_after = "The confusing signs baffled everyone watching."
        metrics = compute_metrics(sample_before, sample_after)
        assert "before" in metrics
        assert "after" in metrics
        assert "change" in metrics
        assert metrics["before"]["word_count"] > 0
        assert metrics["after"]["word_count"] > 0
        assert metrics["after"]["flesch_reading_ease"] > metrics["before"]["flesch_reading_ease"]

    def test_model_complexity_router(self):
        short_text = "This is short."
        assert _select_by_task_complexity(short_text) == "./t5"
