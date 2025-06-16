"""
Module: formatter

Provides Formatter for displaying rule violations.
"""

from typing import Iterable, Any


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
            print(violation)
