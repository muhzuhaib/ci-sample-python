"""Text statistics: unique words, word length, the longest word and reading time."""

from .core import words


def unique_words(text: str) -> int:
    """Return how many different words the text holds."""
    return len(set(words(text)))


def average_word_length(text: str) -> float:
    """Return the mean word length rounded to 2 places, or 0.0 for text without words."""
    found = words(text)
    if not found:
        return 0.0
    return round(sum(len(w) for w in found) / len(found), 2)


def longest_word(text: str) -> str:
    """Return the longest word, the first alphabetically on a tie, or "" for text without words."""
    found = words(text)
    if not found:
        return ""
    return min(found, key=lambda w: (-len(w), w))


def reading_minutes(text: str, words_per_minute: int = 200) -> int:
    """Return the whole minutes needed to read the text at that pace, rounded up."""
    if words_per_minute < 1:
        raise ValueError("words_per_minute must be at least 1")
    return -(-len(words(text)) // words_per_minute)
