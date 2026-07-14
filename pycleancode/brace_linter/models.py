"""
Module: models

Structured result models produced by the analyzer and consumed by
output formatters and the CLI.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from pycleancode.brace_linter.reports.models import FileSummary, NodeReport
from pycleancode.brace_linter.rules.violation_model import RuleViolation


@dataclass
class FileResult:
    """
    Analysis outcome for a single source file.
    """

    file_path: str
    violations: List[RuleViolation]
    summary: FileSummary
    structure: Optional[NodeReport] = None


@dataclass
class AnalysisRun:
    """
    Aggregated outcome of one analyzer invocation across all files.
    """

    results: List[FileResult] = field(default_factory=list)
    parse_errors: List[str] = field(default_factory=list)

    @property
    def files_analyzed(self) -> int:
        """
        Number of files successfully analyzed.
        """
        return len(self.results)

    @property
    def error_count(self) -> int:
        """
        Total error-severity violations across all files.
        """
        return sum(
            1
            for result in self.results
            for violation in result.violations
            if violation.severity == "error"
        )

    @property
    def warning_count(self) -> int:
        """
        Total warning-severity violations across all files.
        """
        return sum(
            1
            for result in self.results
            for violation in result.violations
            if violation.severity == "warning"
        )
