"""Shared pytest fixtures and configuration."""
import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "requires_spacy: mark test as requiring spaCy model")


@pytest.fixture(scope="session")
def spacy_available():
    """Check if spaCy model is available."""
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except (ImportError, OSError):
        return False


def pytest_collection_modifyitems(config, items):
    """Skip tests requiring spaCy if model not available."""
    spacy_available = False
    try:
        import spacy
        spacy.load("en_core_web_sm")
        spacy_available = True
    except (ImportError, OSError):
        pass

    skip_spacy = pytest.mark.skip(reason="spaCy model 'en_core_web_sm' not installed. Run: python -m spacy download en_core_web_sm")

    for item in items:
        if "requires_spacy" in item.keywords and not spacy_available:
            item.add_marker(skip_spacy)
