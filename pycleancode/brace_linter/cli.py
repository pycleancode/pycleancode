"""
Module: cli

Command-line entry point for pycleancode.
"""

import typer
from pycleancode.brace_linter.analyzer import BraceLinterAnalyzer

app = typer.Typer(help="PyCleanCode: Analyze Python code structure and brace depth.")


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Path to file or directory to analyze."),
    config: str = typer.Option(
        "pybrace.yml", "--config", "-c", help="Path to config file."
    ),
    report: bool = typer.Option(
        False, "--report", "-r", help="Generate structural reports."
    ),
) -> None:
    """
    Analyze the given path using pycleancode brace linter.
    """
    analyzer = BraceLinterAnalyzer()
    analyzer.analyze(path, config, report)


def main() -> None:
    """
    Entrypoint to run CLI.
    """
    app()


if __name__ == "__main__":
    main()
