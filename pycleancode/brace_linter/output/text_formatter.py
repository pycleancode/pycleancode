"""
Module: output.text_formatter

Renders AnalysisRun as human-readable console text (the default format).
"""

import io

from rich.console import Console

from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.reports.console_reporter import ConsoleReporter
from pycleancode.brace_linter.reports.depth_chart_reporter import DepthChartReporter
from pycleancode.utils.console import sanitize_console_text


class TextFormatter:
    """
    TextFormatter renders results in the classic pycleancode console style.
    """

    def render(self, run: AnalysisRun) -> str:
        """
        Render the analysis run as plain text.

        Args:
            run (AnalysisRun): Structured analysis results.

        Returns:
            str: Rendered text output.
        """
        buffer = io.StringIO()
        console = Console(file=buffer, width=120)

        for result in run.results:
            self._render_file(console, result)

        for parse_error in run.parse_errors:
            console.print(
                f"error: could not parse {sanitize_console_text(parse_error)}",
                markup=False,
                highlight=False,
            )

        return buffer.getvalue()

    def _render_file(self, console: Console, result: FileResult) -> None:
        safe_path = sanitize_console_text(result.file_path)
        console.print(f"\n🔎 Analyzing: {safe_path}", markup=False, highlight=False)

        for violation in result.violations:
            line = (
                f"{sanitize_console_text(violation.file_path)}:"
                f"{violation.line_number}: "
                f"{sanitize_console_text(violation.message)}"
            )
            console.print(line, markup=False, highlight=False)

        if result.structure is None:
            return

        console.print("\n📊 Structural Report:\n", markup=False, highlight=False)
        ConsoleReporter(console=console).print_tree(result.structure)

        summary = result.summary
        console.print("\n📈 Summary:", markup=False, highlight=False)
        console.print(f"- 🧮 Max Depth: {summary.max_depth}", markup=False)
        console.print(
            f"- 🧬 Nested Functions Depth: {summary.nested_function_depth}",
            markup=False,
        )
        console.print(
            f"- 🚫 Total Violations: {summary.total_violations}", markup=False
        )
        DepthChartReporter(console=console).print_chart(safe_path, summary.max_depth)
