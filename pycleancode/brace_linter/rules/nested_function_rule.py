"""
Module: nested_function_rule

Enforces maximum nested function depth rule.
"""

from typing import List
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.brace_linter.rules.rule_base import RuleBase


class NestedFunctionRule(RuleBase):
    """
    Rule: NestedFunctionRule

    Reports violation if nested function depth exceeds configured maximum.
    """

    def __init__(self, max_nested: int = 1) -> None:
        """
        Initialize NestedFunctionRule.

        Args:
            max_nested (int): Maximum allowed nested function depth. Default is 1.
        """
        self._max_nested = max_nested

    @property
    def name(self) -> str:
        """
        Rule name identifier for configuration.
        """
        return "nested_function"

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
        self._traverse(vbt_root, file_path, 0, violations)
        return violations

    def _traverse(
        self,
        node: VBTNode,
        file_path: str,
        nested_count: int,
        violations: List[RuleViolation],
    ) -> None:
        """
        Recursively traverse VBT tree and collect nested function violations.

        Args:
            node (VBTNode): Current node.
            file_path (str): File path.
            nested_count (int): Current nested count.
            violations (List[RuleViolation]): Accumulator for violations.
        """
        if node.node_type == "FunctionDef":
            nested_count += 1

            if nested_count > self._max_nested:
                violations.append(
                    RuleViolation(
                        file_path=file_path,
                        line_number=node.start_line,
                        message=f"Nested functions depth {nested_count} exceeds allowed {self._max_nested}",
                    )
                )

        for child in node.children:
            self._traverse(child, file_path, nested_count, violations)
