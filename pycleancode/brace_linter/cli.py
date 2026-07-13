"""
Module: cli

Deprecated `pycleancode-brace-linter` entry point. Forwards to the
unified `pycleancode check` implementation.
"""

from typing import Optional

import typer

from pycleancode.cli import run_check

app = typer.Typer(help="[Deprecated] Use `pycleancode check` instead.")

_DEPRECATION_NOTICE = (
    "warning: `pycleancode-brace-linter` is deprecated and will be removed "
    "in 2.0; use `pycleancode check` instead."
)


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Path to file or directory to analyze."),
    config: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to config file."
    ),
    report: bool = typer.Option(
        False, "--report", "-r", help="Generate structural reports."
    ),
) -> None:
    """
    Analyze the given path using pycleancode brace linter.
    """
    typer.echo(_DEPRECATION_NOTICE, err=True)
    raise typer.Exit(
        run_check(
            path=path,
            config=config,
            output_format="text",
            output=None,
            report=report,
        )
    )


def main() -> None:
    """
    Entrypoint to run CLI.
    """
    app()


if __name__ == "__main__":
    main()
