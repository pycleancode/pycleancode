"""
Module: rule_engine

Executes multiple linter rules against a given VBT tree.
"""

from typing import List
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.rules.violation_model import RuleViolation


class RuleEngine:
    """
    RuleEngine executes a collection of rules on parsed VBT trees.
    """

    def __init__(self, rules: List[RuleBase]) -> None:
        """
        Initialize RuleEngine.

        Args:
            rules (List[RuleBase]): List of rule instances to run.
        """
        self.rules = rules

    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        """
        Execute all rules against the given VBT tree.

        Args:
            vbt_root (VBTNode): The root of the Virtual Brace Tree.
            file_path (str): The source file path.

        Returns:
            List[RuleViolation]: Combined list of violations from all rules.
        """
        all_violations: List[RuleViolation] = []

        for rule in self.rules:
            rule_violations = rule.run(vbt_root, file_path)
            all_violations.extend(rule_violations)

        return all_violations
