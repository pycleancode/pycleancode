"""
Module: output.base

Defines the OutputFormatter protocol implemented by all formatters.
"""

from typing import Protocol

from pycleancode.brace_linter.models import AnalysisRun


class OutputFormatter(Protocol):
    """
    Renders an AnalysisRun into a complete output string.
    """

    def render(self, run: AnalysisRun) -> str:
        """
        Render the analysis run.

        Args:
            run (AnalysisRun): Structured analysis results.

        Returns:
            str: The rendered document, ending with a newline.
        """
        ...
