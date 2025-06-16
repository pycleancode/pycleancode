"""
Module: rule_registry

Dynamically discovers and loads all RuleBase subclasses from rules directory.
"""

import os
import importlib
import inspect
from typing import Type, List, Optional
from types import ModuleType
from pycleancode.brace_linter.rules.rule_base import RuleBase


class RuleRegistry:
    """
    RuleRegistry discovers all available rule classes dynamically.
    """

    def __init__(self, rules_path: Optional[str] = None) -> None:
        """
        Initialize RuleRegistry.

        Args:
            rules_path (Optional[str]): Path to rules directory. Defaults to current file directory.
        """
        self.rules_path = rules_path or os.path.dirname(__file__)

    def discover_rules(self) -> List[Type[RuleBase]]:
        """
        Discover all RuleBase subclasses in the rules directory.

        Returns:
            List[Type[RuleBase]]: List of discovered rule classes.
        """
        rules: List[Type[RuleBase]] = []

        for module_name in self._list_rule_modules():
            module = self._import_module(module_name)
            rule_classes = self._extract_rule_classes(module)
            rules.extend(rule_classes)

        return rules

    def _list_rule_modules(self) -> List[str]:
        """
        List all Python rule module filenames (without .py).

        Returns:
            List[str]: Module names.
        """
        return [
            filename[:-3]
            for filename in os.listdir(self.rules_path)
            if filename.endswith(".py") and not filename.startswith("__")
        ]

    def _import_module(self, module_name: str):
        """
        Dynamically import a rule module.

        Args:
            module_name (str): Module filename without extension.

        Returns:
            Module object.
        """
        full_module_path = f"pycleancode.brace_linter.rules.{module_name}"
        return importlib.import_module(full_module_path)

    def _extract_rule_classes(self, module: ModuleType) -> List[Type[RuleBase]]:
        """
        Extract RuleBase subclasses from module.

        Args:
            module: Imported module.

        Returns:
            List[Type[RuleBase]]: List of rule classes.
        """
        return [
            obj
            for _, obj in inspect.getmembers(module, inspect.isclass)
            if issubclass(obj, RuleBase) and obj is not RuleBase
        ]
