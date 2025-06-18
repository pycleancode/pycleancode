import os
import tempfile
import pytest
import yaml
from pycleancode.core.config import ConfigLoader


@pytest.fixture
def config_loader() -> ConfigLoader:
    return ConfigLoader()


def test_load_valid_yaml(config_loader: ConfigLoader) -> None:
    data = """
rules:
  max_depth:
    enabled: true
    max_depth: 3
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", delete=False
    ) as temp_file:
        temp_file.write(data)
        temp_file_path = temp_file.name

    try:
        config = config_loader.load(temp_file_path)
        assert "rules" in config
        assert config["rules"]["max_depth"]["enabled"] is True
        assert config["rules"]["max_depth"]["max_depth"] == 3
    finally:
        os.remove(temp_file_path)


def test_load_empty_file(config_loader: ConfigLoader) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", delete=False
    ) as temp_file:
        temp_file_path = temp_file.name

    try:
        config = config_loader.load(temp_file_path)
        assert config == {}
    finally:
        os.remove(temp_file_path)


def test_file_not_found(config_loader: ConfigLoader) -> None:
    with pytest.raises(FileNotFoundError):
        config_loader.load("non_existing_config.yml")


def test_invalid_yaml(config_loader: ConfigLoader) -> None:
    data = "invalid: [this is: not valid: yaml"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yml", delete=False
    ) as temp_file:
        temp_file.write(data)
        temp_file_path = temp_file.name

    try:
        with pytest.raises(yaml.YAMLError):
            config_loader.load(temp_file_path)
    finally:
        os.remove(temp_file_path)
