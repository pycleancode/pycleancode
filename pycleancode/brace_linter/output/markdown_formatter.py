"""
Module: output.markdown_formatter

Renders AnalysisRun as a pull-request-friendly Markdown summary.
"""

from typing import List

from pycleancode.brace_linter.models import AnalysisRun
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.utils.console import sanitize_console_text


class MarkdownFormatter:
    """
    MarkdownFormatter renders results as a Markdown report.
    """

    def render(self, run: AnalysisRun) -> str:
        """
        Render the analysis run as Markdown.

        Args:
            run (AnalysisRun): Structured analysis results.

        Returns:
            str: Markdown document terminated by a newline.
        """
        lines: List[str] = [
            "# PyCleanCode Report",
            "",
            (
                f"**Files analyzed:** {run.files_analyzed} · "
                f"**Errors:** {run.error_count} · "
                f"**Warnings:** {run.warning_count}"
            ),
            "",
        ]

        violations = sorted(
            (v for result in run.results for v in result.violations),
            key=lambda v: (v.file_path, v.line_number),
        )

        if violations:
            lines.append("| File | Line | Rule | Severity | Message |")
            lines.append("|---|---|---|---|---|")
            lines.extend(self._violation_row(v) for v in violations)
        else:
            lines.append("No violations found.")

        if run.parse_errors:
            lines.append("")
            lines.append("## Parse Errors")
            lines.append("")
            lines.extend(
                f"- {sanitize_console_text(error)}" for error in run.parse_errors
            )

        return "\n".join(lines) + "\n"

    def _violation_row(self, violation: RuleViolation) -> str:
        return (
            f"| {sanitize_console_text(violation.file_path)} "
            f"| {violation.line_number} "
            f"| {violation.rule_name} "
            f"| {violation.severity} "
            f"| {sanitize_console_text(violation.message)} |"
        )
