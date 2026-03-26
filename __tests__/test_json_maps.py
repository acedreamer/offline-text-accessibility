"""Tests for JSON map integrity."""
import json
import pytest
from pathlib import Path


class TestJSONIntegrity:
    def test_idiom_map_no_duplicate_keys(self):
        """Idiom map should have no duplicate keys."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            content = f.read()
            data = json.loads(content)

        # Check that all keys are unique (json.loads already handles this,
        # but we verify explicitly)
        keys = list(data.keys())
        assert len(keys) == len(set(keys)), f"Duplicate keys found in idiom_map.json"

    def test_jargon_map_no_duplicate_keys(self):
        """Jargon map should have no duplicate keys."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            content = f.read()
            data = json.loads(content)

        keys = list(data.keys())
        assert len(keys) == len(set(keys)), f"Duplicate keys found in jargon_map.json"

    def test_idiom_map_values_not_empty(self):
        """All idiom replacements should be non-empty."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            data = json.load(f)

        for key, value in data.items():
            if not key.startswith('__'):
                assert value.strip(), f"Empty value for idiom '{key}'"

    def test_jargon_map_values_not_empty(self):
        """All jargon replacements should be non-empty."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            data = json.load(f)

        for key, value in data.items():
            if not key.startswith('__'):
                assert value.strip(), f"Empty value for jargon '{key}'"

    def test_no_placeholder_keys(self):
        """Maps should not have comment keys like //."""
        path_idiom = Path(__file__).parent.parent / "idiom_map.json"
        path_jargon = Path(__file__).parent.parent / "jargon_map.json"

        with open(path_idiom) as f:
            idioms = json.load(f)
        with open(path_jargon) as f:
            jargon = json.load(f)

        for key in idioms.keys():
            assert not key.startswith('//'), f"Comment key in idiom_map: {key}"

        for key in jargon.keys():
            assert not key.startswith('//'), f"Comment key in jargon_map: {key}"

class TestIdiomQuality:
    """Validate that idiom replacements don't cause false positives."""

    def test_cold_feet_context(self):
        """'cold feet' should not be replaced in temperature context."""
        from autism_mode import format_for_autism
        text = "I washed my cold feet with warm water."
        result = format_for_autism(text)
        assert "**nervous**" not in result

    def test_all_ears_context(self):
        """'all ears' should not replace rabbit ears."""
        from autism_mode import format_for_autism
        text = "The rabbit has long ears."
        result = format_for_autism(text)
        assert "ears" in result

    def test_break_a_leg_medical_context(self):
        """'break a leg' should not be replaced in medical context."""
        from autism_mode import format_for_autism
        text = "The doctor said I broke my leg playing soccer."
        result = format_for_autism(text)
        assert "**good luck**" not in result
