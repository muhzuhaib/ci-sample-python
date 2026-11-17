"""Word counting."""

import re
from collections import Counter

WORD = re.compile(r"[a-z0-9']+")


def words(text: str) -> list[str]:
    """Split text into lowercase words, keeping apostrophes inside words."""
    return [w.strip("'") for w in WORD.findall(text.lower()) if w.strip("'")]


def count_words(text: str) -> int:
    """Return the number of words in the text."""
    return len(words(text))


def top_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    """Return the n most common words with their counts, most common first.

    Ties are broken alphabetically so the result is always the same.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    counts = Counter(words(text))
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]
