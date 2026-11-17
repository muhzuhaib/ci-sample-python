"""Command line entry point."""

import sys

import click

from . import __version__
from .core import count_words, top_words


@click.command()
@click.argument("files", nargs=-1, type=click.File("r", encoding="utf-8"))
@click.option("--top", "-n", default=5, show_default=True, help="How many common words to show.")
@click.version_option(__version__, prog_name="wordtally")
def main(files, top):
    """Count the words in FILES (or standard input) and list the most common ones."""
    text = "\n".join(f.read() for f in files) if files else sys.stdin.read()
    click.echo(f"words: {count_words(text)}")
    for word, count in top_words(text, top):
        click.echo(f"{count:>6}  {word}")
