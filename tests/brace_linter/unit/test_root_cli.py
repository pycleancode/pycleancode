import json
from pathlib import Path

from typer.testing import CliRunner

from pycleancode.cli import app

runner = CliRunner(mix_stderr=False)

CLEAN_SOURCE = "def fine():\n    pass\n"
DEEP_SOURCE = """
def outer():
    def inner():
        def too_deep():
            def more():
                pass
"""
WARNING_ONLY_CONFIG = """
rules:
  max_depth:
    enabled: true
    max_depth: 3
    severity: warning
  nested_function:
    enabled: true
    max_nested: 1
    severity: warning
"""


def _write(tmp_path: Path, name: str, content: str) -> Path:
    target = tmp_path / name
    target.write_text(content)
    return target


def test_check_clean_file_exits_zero(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)  # avoid picking up the repo's own pybrace.yml
    source = _write(tmp_path, "clean.py", CLEAN_SOURCE)
    result = runner.invoke(app, ["check", str(source)])
    assert result.exit_code == 0
    assert "🔎 Analyzing:" in result.stdout


def test_check_violations_exit_one(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "deep.py", DEEP_SOURCE)
    result = runner.invoke(app, ["check", str(source)])
    assert result.exit_code == 1
    assert "Depth 4 exceeds max 3" in result.stdout


def test_check_warnings_only_exit_zero(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "deep.py", DEEP_SOURCE)
    config = _write(tmp_path, "warn.yml", WARNING_ONLY_CONFIG)
    result = runner.invoke(app, ["check", str(source), "--config", str(config)])
    assert result.exit_code == 0


def test_check_missing_config_exits_two(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "clean.py", CLEAN_SOURCE)
    result = runner.invoke(app, ["check", str(source), "--config", "absent.yml"])
    assert result.exit_code == 2
    assert "error:" in result.stderr


def test_check_unknown_format_exits_two(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "clean.py", CLEAN_SOURCE)
    result = runner.invoke(app, ["check", str(source), "--format", "xml"])
    assert result.exit_code == 2
    assert "unknown format" in result.stderr


def test_check_parse_error_exits_two(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "bad.py", "def broken(:\n")
    result = runner.invoke(app, ["check", str(source)])
    assert result.exit_code == 2


def test_check_json_format(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "deep.py", DEEP_SOURCE)
    result = runner.invoke(app, ["check", str(source), "--format", "json"])
    payload = json.loads(result.stdout)
    assert payload["schemaVersion"] == 1
    assert payload["summary"]["errors"] > 0


def test_check_output_writes_file(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    source = _write(tmp_path, "deep.py", DEEP_SOURCE)
    out_file = tmp_path / "report.md"
    result = runner.invoke(
        app,
        ["check", str(source), "--format", "markdown", "--output", str(out_file)],
    )
    assert result.exit_code == 1
    assert out_file.read_text().startswith("# PyCleanCode Report")
    assert result.stdout == ""


def test_version_flag(tmp_path) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "pycleancode" in result.stdout
