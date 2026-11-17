from click.testing import CliRunner

from wordtally.cli import main


def test_cli_reads_standard_input():
    result = CliRunner().invoke(main, ["--top", "1"], input="red red blue")
    assert result.exit_code == 0
    assert result.output.splitlines() == ["words: 3", "     2  red"]


def test_cli_reads_files(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("sun moon sun", encoding="utf-8")
    result = CliRunner().invoke(main, [str(f)])
    assert result.exit_code == 0
    assert "words: 3" in result.output
