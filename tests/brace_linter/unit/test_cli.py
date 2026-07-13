from typer.testing import CliRunner

from pycleancode.brace_linter.cli import app

runner = CliRunner(mix_stderr=False)

DEEP_SOURCE = """
def outer():
    def inner():
        def too_deep():
            def more():
                pass
"""


def test_cli_runs_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_cli_prints_deprecation_and_forwards(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "deep.py"
    source.write_text(DEEP_SOURCE)

    result = runner.invoke(app, [str(source)])

    assert "deprecated" in result.stderr
    assert "pycleancode check" in result.stderr
    assert "Depth 4 exceeds max 3" in result.stdout
    assert result.exit_code == 1  # violations now fail, per 1.1.0 contract


def test_cli_clean_file_exits_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "clean.py"
    source.write_text("def fine():\n    pass\n")

    result = runner.invoke(app, [str(source)])
    assert result.exit_code == 0
