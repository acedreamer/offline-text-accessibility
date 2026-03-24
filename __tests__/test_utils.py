"""Tests for utility functions."""
import pytest

from utils import split_sentences, get_words, count_syllables


# ==================== split_sentences Tests ====================

def test_split_sentences_basic():
    """Test basic sentence splitting."""
    text = "Hello world. This is a test! How are you?"
    result = split_sentences(text)
    assert len(result) == 3
    assert result[0] == "Hello world."
    assert result[1] == "This is a test!"
    assert result[2] == "How are you?"


def test_split_sentences_single():
    """Test single sentence."""
    text = "This is a single sentence."
    result = split_sentences(text)
    assert len(result) == 1
    assert result[0] == "This is a single sentence."


def test_split_sentences_empty():
    """Test empty string returns empty list."""
    result = split_sentences("")
    assert result == []


def test_split_sentences_whitespace_only():
    """Test whitespace-only string returns empty list."""
    result = split_sentences("   \n\t  ")
    assert result == []


def test_split_sentences_abbreviations():
    """Test that common abbreviations don't split sentences."""
    text = "Dr. Smith went to the U.S.A. on Jan. 5. He met Mr. Jones."
    result = split_sentences(text)
    # Should be 2 sentences: "Dr. Smith went to the U.S.A. on Jan. 5." and "He met Mr. Jones."
    assert len(result) == 2
    assert result[0] == "Dr. Smith went to the U.S.A. on Jan. 5."
    assert result[1] == "He met Mr. Jones."


def test_split_sentences_multiple_abbreviations():
    """Test various abbreviations are handled correctly."""
    text = "Prof. Einstein worked at NASA. He met Dr. Brown and Mrs. Davis."
    result = split_sentences(text)
    assert len(result) == 2
    assert "Prof. Einstein" in result[0]
    assert "Dr. Brown" in result[1]
    assert "Mrs. Davis" in result[1]


def test_split_sentences_decimal_numbers():
    """Test decimal numbers are not split."""
    text = "The value is 3.14. Another number is 2.718."
    result = split_sentences(text)
    assert len(result) == 2
    assert result[0] == "The value is 3.14."
    assert result[1] == "Another number is 2.718."


def test_split_sentences_volume_patterns():
    """Test volume/page patterns like 'Vol. 5, pp. 23-45'."""
    text = "See Vol. 5, pp. 23-45. Also check pg. 10."
    result = split_sentences(text)
    assert len(result) == 2
    assert "Vol. 5" in result[0] or "Vol. 5," in result[0]
    assert "pp. 23-45" in result[0] or "pp. 23-45" in result[0]
    assert "pg. 10" in result[1]


def test_split_sentences_am_pm():
    """Test a.m. and p.m. abbreviations."""
    text = "The store opens at 9 a.m. It closes at 5 p.m."
    result = split_sentences(text)
    assert len(result) == 2
    assert "9 a.m." in result[0]
    assert "5 p.m." in result[1]


def test_split_sentences_ellipsis():
    """Test ellipsis (...) does not interfere with splitting."""
    text = "Wait... what? I'm not sure..."
    result = split_sentences(text)
    assert len(result) == 2
    assert result[0] == "Wait... what?"
    assert result[1] == "I'm not sure..."


def test_split_sentences_multiple_punctuation():
    """Test multiple punctuation marks at end."""
    text = "What?! Really... Yes!!!"
    result = split_sentences(text)
    assert len(result) == 3
    assert result[0] == "What?!"
    assert result[1] == "Really..."
    assert result[2] == "Yes!!!"


def test_split_sentences_numbered_list():
    """Test numbered list items are split correctly."""
    text = "1. First item. 2. Second item. 3. Third item."
    result = split_sentences(text)
    assert len(result) == 3
    assert "First item" in result[0]
    assert "Second item" in result[1]
    assert "Third item" in result[2]


def test_split_sentences_quotes():
    """Test sentences with quoted text."""
    text = 'He said "Hello." Then he left.'
    result = split_sentences(text)
    assert len(result) == 2
    assert '"Hello."' in result[0] or 'He said "Hello."' in result[0]
    assert "Then he left." in result[1]


def test_split_sentences_preserves_spacing():
    """Test that extra spaces are handled."""
    text = "Hello world.   This is a test.  "
    result = split_sentences(text)
    assert len(result) == 2
    assert result[0] == "Hello world."
    assert result[1] == "This is a test."


# ==================== count_syllables Tests ====================

def test_count_syllables_basic_one():
    """Test single syllable words."""
    assert count_syllables("cat") == 1
    assert count_syllables("dog") == 1
    assert count_syllables("the") == 1
    assert count_syllables("a") == 1
    assert count_syllables("I") == 1


def test_count_syllables_basic_multiple():
    """Test multi-syllable words."""
    assert count_syllables("hello") == 2  # hel-lo
    assert count_syllables("world") == 1
    assert count_syllables("beautiful") == 3  # beau-ti-ful
    assert count_syllables("education") == 4  # ed-u-ca-tion
    assert count_syllables("computer") == 3  # com-pu-ter


def test_count_syllables_silent_e():
    """Test words with silent e at the end."""
    assert count_syllables("make") == 1
    assert count_syllables("take") == 1
    assert count_syllables("bake") == 1
    assert count_syllables("like") == 1
    assert count_syllables("home") == 1
    assert count_syllables("time") == 1
    assert count_syllables("use") == 1  # u-se? Actually "use" is 1 syllable, but the algorithm: "use" -> remove silent e -> "us" -> 1 vowel group -> 1


def test_count_syllables_le_ending():
    """Test words ending in 'le' that should add syllable."""
    assert count_syllables("table") == 2  # ta-ble
    assert count_syllables("little") == 2  # lit-tle
    assert count_syllables("cable") == 2  # ca-ble
    assert count_syllables("bottle") == 2  # bot-tle
    assert count_syllables("apple") == 2  # ap-ple


def test_count_syllables_le_exceptions():
    """Test words ending in 'le' where consonant is also a vowel or special."""
    # "able" ends with 'le' but 'a' is vowel before, so should not add extra?
    # The algorithm checks: word.endswith('le') and len(word) > 2 and word[-3] not in vowels
    # "able": word[-3] = 'b' (not vowel) -> will add +1
    # count_syllables("able") -> after removing e? Actually code: only remove silent e if not ending with 'le'...
    # Let's check implementation: it removes silent e before counting if word ends with 'e' and NOT with 'le' or 'me'
    # So for "able": it ends with 'e' but also 'le'? word.endswith('le') is True, so it does NOT remove the e.
    # So "able" = a-b-le. Vowel groups: 'a' (1), 'e' (1?) Actually 'e' is vowel but after consonant? Let's trace:
    # word = "able" -> not removed e
    # count vowel groups: a (1), e (since prev not vowel, count becomes 2). That's 2.
    # Then if word.endswith('le') and word[-3] not in vowels: 'a' is vowel, so condition false -> no extra add.
    # returns max(1, 2) = 2. So "able" is 2 syllables.
    assert count_syllables("able") == 2


def test_count_syllables_y_as_vowel():
    """Test words where 'y' acts as vowel."""
    assert count_syllables("sky") == 1
    assert count_syllables("fly") == 1
    assert count_syllables("my") == 1
    assert count_syllables("cry") == 1
    assert count_syllables("happy") == 2  # hap-py
    assert count_syllables("silly") == 2  # sil-ly


def test_count_syllables_compound_vowels():
    """Test vowel groups are counted once."""
    assert count_syllables("see") == 1  # 'ee' is one group
    assert count_syllables("feed") == 1
    assert count_syllables("boat") == 1  # 'oa' one group
    assert count_syllables("rain") == 1  # 'ai' one group
    assert count_syllables("free") == 1


def test_count_syllables_short_words():
    """Test words with 3 or fewer letters always return at least 1."""
    assert count_syllables("") == 0
    assert count_syllables("a") == 1
    assert count_syllables("I") == 1
    assert count_syllables("to") == 1
    assert count_syllables("the") == 1
    assert count_syllables("and") == 1
    assert count_syllables("but") == 1


def test_count_syllables_case_insensitive():
    """Test case does not affect syllable count."""
    assert count_syllables("HELLO") == 2
    assert count_syllables("Hello") == 2
    assert count_syllables("hello") == 2


def test_count_syllables_with_punctuation():
    """Test words with punctuation are handled."""
    assert count_syllables("hello!") == 2
    assert count_syllables("world.") == 1
    assert count_syllables("'hello'") == 2  # quotes should be stripped by non-alpha removal


def test_count_syllables_edge_cases():
    """Test various edge cases."""
    # Words with non-alphabetic characters mixed in (should strip them)
    assert count_syllables("he--llo") >= 1
    # Empty after stripping
    assert count_syllables("123") == 0
    # Single vowel
    assert count_syllables("eye") == 1  # 'e' group, then 'e'? actually eye: e-y-e? Let's trace: e (1), y (is vowel? according to code 'aeiouy' includes y, so y is vowel -> but prev was e (vowel), so not counted. e at end: prev y (vowel) so not counted. So total = 1? Actually count algorithm: prev_is_vowel = False initially. char 'e': is_vowel True, and not prev, so count=1, prev=True. Next 'y': is_vowel True, prev True -> no increment. Next 'e': is_vowel True, prev True -> no increment. So count=1. So "eye" is 1 syllable under this algorithm. That's actually correct (eye = 1 syllable). So it passes.


# ==================== get_words Tests ====================

def test_get_words_basic():
    """Test basic word extraction."""
    text = "Hello world, this is a test."
    result = get_words(text)
    expected = ["Hello", "world", "this", "is", "a", "test"]
    assert result == expected


def test_get_words_hyphenated():
    """Test hyphenated compounds are kept together."""
    text = "mother-in-law and well-known author"
    result = get_words(text)
    assert "mother-in-law" in result
    assert "well-known" in result


def test_get_words_contractions():
    """Test contractions are expanded."""
    text = "I can't go. He won't attend. They didn't know."
    result = get_words(text)
    # After expansion, should contain expanded forms
    assert "cannot" in result
    assert "will" in result or "will not" in result or "willnot" in result  # actually "won't" -> "will not" - but expansion replaces individual words? Let's check implementation: contractions dict maps to multi-word expansions. The replacement is: for each contraction, replace with expansion. That would put spaces in. So "won't" -> "will not". So result would contain "will", "not". So we can check for "will" and "not"
    assert "not" in result
    assert "did" in result
    assert "know" in result


def test_get_words_apostrophe_possessives():
    """Test possessives and apostrophe words are kept."""
    text = "John's book and the cat's toy."
    result = get_words(text)
    assert "John's" in result
    assert "cat's" in result


def test_get_words_empty():
    """Test empty string returns empty list."""
    result = get_words("")
    assert result == []


def test_get_words_numbers():
    """Test numbers are not extracted as words."""
    text = "There are 123 apples and 456 oranges."
    result = get_words(text)
    # Should not include "123" or "456" (digits only)
    for word in result:
        assert not word.isdigit()


def test_get_words_mixed_case():
    """Test case preservation."""
    text = "Hello World"
    result = get_words(text)
    assert "Hello" in result
    assert "World" in result
