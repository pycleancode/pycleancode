"""
Module: formatter

Provides Formatter for displaying rule violations.
"""

from typing import Iterable, Any
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.utils.console import sanitize_console_text


class Formatter:
    """
    Formatter outputs violations in a simple textual format.
    """

    @staticmethod
    def format(violations: Iterable[Any]) -> None:
        """
        Format and print each violation.

        Args:
            violations (Iterable[Any]): List of violations to display.
        """
        for violation in violations:
            if isinstance(violation, RuleViolation):
                safe_file_path = sanitize_console_text(violation.file_path)
                print(f"{safe_file_path}:{violation.line_number}: {violation.message}")
                continue

            print(sanitize_console_text(violation))
