"""
Module: max_depth_rule

Enforces maximum depth limit on code structure.
"""

from typing import List
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.brace_linter.rules.rule_base import RuleBase


class MaxDepthRule(RuleBase):
    """
    Rule: MaxDepthRule

    Reports violation if node depth exceeds configured maximum depth.
    """

    def __init__(self, max_depth: int = 3) -> None:
        """
        Initialize MaxDepthRule.

        Args:
            max_depth (int): Maximum allowed depth. Default is 3.
        """
        self._max_depth = max_depth

    @property
    def name(self) -> str:
        """
        Rule name identifier for configuration.
        """
        return "max_depth"

    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        """
        Execute rule on given VBT tree.

        Args:
            vbt_root (VBTNode): The root node to analyze.
            file_path (str): File path for violation reporting.

        Returns:
            List[RuleViolation]: List of violations found.
        """
        violations: List[RuleViolation] = []
        self._traverse(vbt_root, file_path, 1, violations)
        return violations

    def _traverse(
        self, node: VBTNode, file_path: str, depth: int, violations: List[RuleViolation]
    ) -> None:
        """
        Recursively traverse VBT tree and collect violations.

        Args:
            node (VBTNode): Current node.
            file_path (str): File path.
            depth (int): Current depth.
            violations (List[RuleViolation]): Accumulator for violations.
        """
        if depth > self._max_depth:
            violations.append(
                RuleViolation(
                    file_path=file_path,
                    line_number=node.start_line,
                    message=f"Depth {depth} exceeds max {self._max_depth}",
                )
            )

        for child in node.children:
            self._traverse(child, file_path, depth + 1, violations)
