"""
Module: violation_model

Defines the RuleViolation data structure used for rule violations.
"""

from dataclasses import dataclass


@dataclass
class RuleViolation:
    file_path: str
    line_number: int
    message: str

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}: {self.message}"
