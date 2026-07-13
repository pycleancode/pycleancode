"""
Module: config_loader

Provides ConfigLoader for loading YAML configuration files and
ConfigResolver for layered configuration discovery.
"""

import copy
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

try:  # Python >= 3.11
    import tomllib
except ModuleNotFoundError:  # Python 3.9 / 3.10
    import tomli as tomllib  # type: ignore[no-redef]

from pycleancode.brace_linter.exceptions.errors import ConfigError
from pycleancode.brace_linter.rules.violation_model import (
    DEFAULT_SEVERITY,
    VALID_SEVERITIES,
)

DEFAULT_CONFIG: Dict[str, Any] = {
    "rules": {
        "max_depth": {"enabled": True, "max_depth": 3},
        "nested_function": {"enabled": True, "max_nested": 1},
    }
}


class ConfigLoader:
    """
    ConfigLoader is responsible for loading configuration data from YAML files.

    It reads a given YAML file and parses its content into a Python dictionary.
    """

    def __init__(self, parser: Any = yaml.safe_load) -> None:
        """
        Initialize ConfigLoader with a YAML parser.
        Allows dependency injection for better testability.
        """
        self._parser = parser

    def load(self, config_path: str) -> Dict[str, Any]:
        """
        Load the configuration from the given file path.

        Args:
            config_path (str): The path to the YAML configuration file.

        Returns:
            dict: The parsed YAML configuration.

        Raises:
            FileNotFoundError: If the file does not exist.
            yaml.YAMLError: If YAML parsing fails.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config = self._parser(file)
                return config if config is not None else {}
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {config_path}") from e
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML format in file: {config_path}") from e


class ConfigResolver:
    """
    ConfigResolver discovers and validates rule configuration from,
    in order: an explicit path, ./pybrace.yml, [tool.pycleancode] in
    ./pyproject.toml, or built-in defaults. No parent-directory walk-up.
    """

    def __init__(
        self,
        loader: Optional[ConfigLoader] = None,
        cwd: Optional[Path] = None,
    ) -> None:
        """
        Initialize ConfigResolver.

        Args:
            loader (Optional[ConfigLoader]): YAML loader (injectable for tests).
            cwd (Optional[Path]): Directory to discover config in.
                Defaults to the process working directory.
        """
        self._loader = loader or ConfigLoader()
        self._cwd = cwd or Path.cwd()

    def resolve(self, explicit_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Resolve configuration using the layered discovery order.

        Args:
            explicit_path (Optional[str]): --config value, if given.

        Returns:
            Dict[str, Any]: Validated configuration dictionary.

        Raises:
            FileNotFoundError: If explicit_path is given but missing.
            ConfigError: If any discovered config is invalid.
        """
        if explicit_path is not None:
            return self._validated(self._loader.load(explicit_path), explicit_path)

        yaml_path = self._cwd / "pybrace.yml"
        if yaml_path.is_file():
            return self._validated(self._loader.load(str(yaml_path)), str(yaml_path))

        section = self._pyproject_section()
        if section is not None:
            return self._validated(section, str(self._cwd / "pyproject.toml"))

        return copy.deepcopy(DEFAULT_CONFIG)

    def _pyproject_section(self) -> Optional[Dict[str, Any]]:
        pyproject_path = self._cwd / "pyproject.toml"
        if not pyproject_path.is_file():
            return None

        try:
            with open(pyproject_path, "rb") as file:
                data = tomllib.load(file)
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"Invalid TOML in {pyproject_path}: {exc}") from exc

        section: Optional[Dict[str, Any]] = data.get("tool", {}).get("pycleancode")
        return section

    def _validated(self, config: Dict[str, Any], source: str) -> Dict[str, Any]:
        rules = config.get("rules", {})
        if not isinstance(rules, dict):
            raise ConfigError(f"'rules' must be a mapping in {source}")

        for rule_name, rule_conf in rules.items():
            if not isinstance(rule_conf, dict):
                raise ConfigError(f"Rule '{rule_name}' must be a mapping in {source}")

            severity = rule_conf.get("severity", DEFAULT_SEVERITY)
            if severity not in VALID_SEVERITIES:
                raise ConfigError(
                    f"Invalid severity {severity!r} for rule '{rule_name}' "
                    f"in {source}; expected one of {VALID_SEVERITIES}"
                )

            enabled = rule_conf.get("enabled", False)
            if not isinstance(enabled, bool):
                raise ConfigError(
                    f"'enabled' for rule '{rule_name}' must be a boolean "
                    f"in {source}"
                )

            for key, value in rule_conf.items():
                if key in ("enabled", "severity"):
                    continue
                if isinstance(value, bool) or not isinstance(value, int):
                    raise ConfigError(
                        f"Option '{key}' for rule '{rule_name}' must be an "
                        f"integer in {source}, got {value!r}"
                    )

        return config
