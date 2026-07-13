"""
Module: violation_model

Defines the RuleViolation data structure used for rule violations.
"""

from dataclasses import dataclass
from typing import Literal, Tuple

Severity = Literal["error", "warning"]

DEFAULT_SEVERITY: Severity = "error"
VALID_SEVERITIES: Tuple[str, ...] = ("error", "warning")


@dataclass
class RuleViolation:
    file_path: str
    line_number: int
    message: str
    rule_name: str = ""
    severity: Severity = DEFAULT_SEVERITY

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}: {self.message}"
