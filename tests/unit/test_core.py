import pytest

from wordtally.core import count_words, top_words, words


def test_words_are_lowercased_and_split():
    assert words("Hello, hello WORLD!") == ["hello", "hello", "world"]


def test_apostrophes_inside_words_are_kept():
    assert words("It's 'quoted' don't") == ["it's", "quoted", "don't"]


def test_count_words_on_empty_text_is_zero():
    assert count_words("") == 0


def test_count_words():
    assert count_words("one two three, four") == 4


def test_top_words_orders_by_count_then_alphabet():
    text = "b a c a b a"
    assert top_words(text, 2) == [("a", 3), ("b", 2)]
    assert top_words("y x", 2) == [("x", 1), ("y", 1)]


def test_top_words_rejects_n_below_one():
    with pytest.raises(ValueError):
        top_words("a", 0)
