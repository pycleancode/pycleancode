from typer.testing import CliRunner
from pycleancode.brace_linter.cli import app

runner = CliRunner()


def test_cli_runs_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
