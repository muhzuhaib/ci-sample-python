"""Count words in text and show the most common ones."""

from importlib.metadata import version

from .core import count_words, top_words

__all__ = ["count_words", "top_words", "__version__"]
__version__ = version("wordtally")
