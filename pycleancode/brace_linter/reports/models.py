"""
Module: reports.models

Defines core dataclasses for linter reporting.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class NodeReport:
    """
    Represents a node in the parsed code structure with its depth and children.
    """

    node_type: str
    start_line: int
    depth: int
    children: List["NodeReport"] = field(default_factory=list)


@dataclass
class FileSummary:
    """
    Summarizes analysis results for a single source file.
    """

    file_path: str
    max_depth: int
    nested_function_depth: int
    total_violations: int
