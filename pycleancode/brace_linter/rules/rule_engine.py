"""
Module: rule_engine

Executes multiple linter rules against a given VBT tree.
"""

from typing import Dict, List, Optional
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.rules.violation_model import (
    DEFAULT_SEVERITY,
    RuleViolation,
)


class RuleEngine:
    """
    RuleEngine executes a collection of rules on parsed VBT trees.
    """

    def __init__(
        self,
        rules: List[RuleBase],
        severities: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize RuleEngine.

        Args:
            rules (List[RuleBase]): List of rule instances to run.
            severities (Optional[Dict[str, str]]): Severity per rule name.
        """
        self.rules = rules
        self.severities = severities or {}

    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        """
        Execute all rules against the given VBT tree.

        Args:
            vbt_root (VBTNode): The root of the Virtual Brace Tree.
            file_path (str): The source file path.

        Returns:
            List[RuleViolation]: Combined list of violations from all rules,
            stamped with the producing rule's name and configured severity.
        """
        all_violations: List[RuleViolation] = []

        for rule in self.rules:
            severity = self.severities.get(rule.name, DEFAULT_SEVERITY)
            rule_violations = rule.run(vbt_root, file_path)

            for violation in rule_violations:
                violation.rule_name = rule.name
                violation.severity = severity  # type: ignore[assignment]

            all_violations.extend(rule_violations)

        return all_violations
