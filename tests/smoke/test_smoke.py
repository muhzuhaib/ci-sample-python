"""Five smoke tests, run against the built wheel installed in a clean environment."""

import subprocess
import sys

import wordtally


def run(*args, stdin=""):
    return subprocess.run(
        [sys.executable, "-m", "wordtally", *args],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def test_package_imports_from_the_installed_wheel():
    assert "site-packages" in wordtally.__file__


def test_version_matches_the_package_metadata():
    out = run("--version")
    assert out.returncode == 0
    assert wordtally.__version__ in out.stdout


def test_help_runs():
    assert run("--help").returncode == 0


def test_counts_words_from_standard_input():
    out = run("--top", "1", stdin="a b a")
    assert out.returncode == 0
    assert out.stdout.splitlines()[0] == "words: 3"


def test_bad_option_fails_cleanly():
    out = run("--top", "not-a-number")
    assert out.returncode == 2
