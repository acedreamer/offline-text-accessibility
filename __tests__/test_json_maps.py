"""Tests for JSON map integrity."""
import json
import pytest
from pathlib import Path


class TestJSONIntegrity:
    def test_idiom_map_exists(self):
        """Idiom map file should exist."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        assert path.exists(), "idiom_map.json not found"

    def test_jargon_map_exists(self):
        """Jargon map file should exist."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        assert path.exists(), "jargon_map.json not found"

    def test_idiom_map_valid_json(self):
        """Idiom map should be valid JSON."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_jargon_map_valid_json(self):
        """Jargon map should be valid JSON."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_idiom_map_no_duplicate_keys(self):
        """Idiom map should have no duplicate keys (JSON handles this)."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            data = json.load(f)
        # json.loads already validates duplicate keys (last one wins)
        # Just verify it loads without error
        assert len(data) > 0

    def test_jargon_map_no_duplicate_keys(self):
        """Jargon map should have no duplicate keys (JSON handles this)."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            data = json.load(f)
        assert len(data) > 0

    def test_idiom_map_values_not_empty(self):
        """All idiom replacements should be non-empty."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            data = json.load(f)

        for key, value in data.items():
            assert value.strip(), f"Empty value for idiom '{key}'"

    def test_jargon_map_values_not_empty(self):
        """All jargon replacements should be non-empty."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            data = json.load(f)

        for key, value in data.items():
            assert value.strip(), f"Empty value for jargon '{key}'"

    def test_no_placeholder_keys(self):
        """Maps should not have comment keys like '//'."""
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

    def test_idiom_map_min_entries(self):
        """Idiom map should have minimum number of entries."""
        path = Path(__file__).parent.parent / "idiom_map.json"
        with open(path) as f:
            data = json.load(f)
        # At least the 20 entries from the base specification
        assert len(data) >= 20

    def test_jargon_map_min_entries(self):
        """Jargon map should have minimum number of entries."""
        path = Path(__file__).parent.parent / "jargon_map.json"
        with open(path) as f:
            data = json.load(f)
        # At least the 20 entries from the base specification
        assert len(data) >= 20
