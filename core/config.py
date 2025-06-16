"""
Module: config_loader

Provides ConfigLoader class for loading YAML configuration files with safe parsing and error handling.
"""

import yaml
from typing import Any, Dict


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
