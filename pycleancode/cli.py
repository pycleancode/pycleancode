"""
Module: cli

Root command-line entry point for pycleancode.
"""

from importlib import metadata
from pathlib import Path
from typing import Dict, Optional, Type

import typer
import yaml

from pycleancode.brace_linter.analyzer import BraceLinterAnalyzer
from pycleancode.brace_linter.exceptions.errors import ConfigError
from pycleancode.brace_linter.output import (
    JsonFormatter,
    MarkdownFormatter,
    TextFormatter,
)
from pycleancode.core.config import ConfigResolver

app = typer.Typer(help="PyCleanCode: maintainability checks for Python code.")

FORMATTERS: Dict[str, Type] = {
    "text": TextFormatter,
    "json": JsonFormatter,
    "markdown": MarkdownFormatter,
}


def run_check(
    path: str,
    config: Optional[str],
    output_format: str,
    output: Optional[str],
    report: bool,
) -> int:
    """
    Shared implementation behind `pycleancode check` and the deprecated
    `pycleancode-brace-linter` shim.

    Returns:
        int: Process exit code (0 clean/warnings, 1 errors, 2 failure).
    """
    if output_format not in FORMATTERS:
        typer.echo(
            f"error: unknown format {output_format!r} "
            f"(choose from: {', '.join(sorted(FORMATTERS))})",
            err=True,
        )
        return 2

    try:
        resolved = ConfigResolver().resolve(config)
        run = BraceLinterAnalyzer().analyze(path, resolved, report)
        rendered = FORMATTERS[output_format]().render(run)

        if output is not None:
            Path(output).write_text(rendered, encoding="utf-8")
        else:
            typer.echo(rendered, nl=False)
    except (ConfigError, FileNotFoundError, yaml.YAMLError, OSError) as exc:
        typer.echo(f"error: {exc}", err=True)
        return 2

    if run.parse_errors:
        return 2
    if run.error_count > 0:
        return 1
    return 0


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pycleancode {metadata.version('pycleancode')}")
        raise typer.Exit(0)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the pycleancode version and exit.",
    ),
) -> None:
    """
    PyCleanCode command-line interface.
    """


@app.command()
def check(
    path: str = typer.Argument(..., help="Path to file or directory to analyze."),
    config: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to config file (YAML)."
    ),
    output_format: str = typer.Option(
        "text", "--format", "-f", help="Output format: text, json, or markdown."
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Write output to this file instead of stdout."
    ),
    report: bool = typer.Option(
        False, "--report", "-r", help="Include structural report (text format only)."
    ),
) -> None:
    """
    Analyze Python code for maintainability violations.
    """
    raise typer.Exit(
        run_check(
            path=path,
            config=config,
            output_format=output_format,
            output=output,
            report=report,
        )
    )
