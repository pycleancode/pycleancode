"""
Module: rule_loader

Loads and instantiates linter rules dynamically based on configuration.
"""

from typing import List, Dict, Type, Any
from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.rules.registry import RuleRegistry


class RuleLoader:
    """
    RuleLoader dynamically loads and configures rule instances based on provided config.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize RuleLoader.

        Args:
            config (Dict): The full configuration dictionary.
        """
        self.config = config
        self.registry = RuleRegistry()

    def load_rules(self) -> List[RuleBase]:
        """
        Discover and load all enabled rules from registry and config.

        Returns:
            List[RuleBase]: Instantiated list of enabled rule objects.
        """
        loaded_rules: List[RuleBase] = []
        rule_classes = self.registry.discover_rules()
        rules_config = self.config.get("rules", {})

        for rule_cls in rule_classes:
            rule_name = self._get_rule_name(rule_cls)
            rule_conf = rules_config.get(rule_name, {})

            if not rule_conf.get("enabled", False):
                continue

            rule_instance = self._instantiate_rule(rule_cls, rule_conf)
            loaded_rules.append(rule_instance)

        return loaded_rules

    def _get_rule_name(self, rule_cls: Type[RuleBase]) -> str:
        """
        Instantiate rule class to get its name.
        """
        return rule_cls().name

    def _instantiate_rule(
        self, rule_cls: Type[RuleBase], rule_conf: Dict[str, Any]
    ) -> RuleBase:
        """
        Instantiate rule class dynamically based on config.

        Supports rules with or without config parameters.

        Args:
            rule_cls: The rule class type.
            rule_conf: Configuration dictionary for the rule.

        Returns:
            RuleBase: The instantiated rule object.
        """
        try:
            return rule_cls(**rule_conf)
        except TypeError:
            return rule_cls()
