import pytest

from wordtally.stats import average_word_length, longest_word, reading_minutes, unique_words


def test_unique_words_counts_each_word_once():
    assert unique_words("The cat and the hat, the end") == 5


def test_average_word_length_is_rounded_and_zero_for_empty_text():
    assert average_word_length("ab abcd") == 3.0
    assert average_word_length("a bb bb") == 1.67
    assert average_word_length("  ...  ") == 0.0


def test_longest_word_breaks_ties_alphabetically():
    assert longest_word("pear apple fig plums") == "apple"
    assert longest_word("") == ""


def test_reading_minutes_rounds_up():
    assert reading_minutes("word " * 401) == 3
    assert reading_minutes("one two", words_per_minute=2) == 1
    assert reading_minutes("") == 0


def test_reading_minutes_rejects_a_pace_below_one():
    with pytest.raises(ValueError):
        reading_minutes("a", words_per_minute=0)
