"""
Module: rule_base

Defines the abstract base class for all linter rules.
"""

from abc import ABC, abstractmethod
from typing import List
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation


class RuleBase(ABC):
    """
    Abstract base class for all rule implementations.

    All rules must implement 'run' and 'name' interface.
    """

    @abstractmethod
    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        """
        Execute the rule on the given VBT tree.

        Args:
            vbt_root (VBTNode): The root node of the parsed file.
            file_path (str): Path to the source file.

        Returns:
            List[RuleViolation]: List of rule violations found.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique name of the rule (used for configuration & reporting).
        """
        ...
