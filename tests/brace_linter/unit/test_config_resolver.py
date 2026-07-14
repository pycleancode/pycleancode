from pathlib import Path

import pytest

from pycleancode.brace_linter.exceptions.errors import ConfigError
from pycleancode.core.config import DEFAULT_CONFIG, ConfigResolver

YAML_CONFIG = """
rules:
  max_depth:
    enabled: true
    max_depth: 2
"""

PYPROJECT_WITH_SECTION = """
[tool.pycleancode.rules.max_depth]
enabled = true
max_depth = 4
severity = "warning"
"""

PYPROJECT_WITHOUT_SECTION = """
[tool.poetry]
name = "irrelevant"
"""


def test_explicit_config_wins(tmp_path: Path) -> None:
    explicit = tmp_path / "custom.yml"
    explicit.write_text(YAML_CONFIG)
    (tmp_path / "pybrace.yml").write_text("rules: {}")

    config = ConfigResolver(cwd=tmp_path).resolve(str(explicit))
    assert config["rules"]["max_depth"]["max_depth"] == 2


def test_explicit_config_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        ConfigResolver(cwd=tmp_path).resolve(str(tmp_path / "absent.yml"))


def test_pybrace_yml_discovered(tmp_path: Path) -> None:
    (tmp_path / "pybrace.yml").write_text(YAML_CONFIG)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT_WITH_SECTION)

    config = ConfigResolver(cwd=tmp_path).resolve()
    assert config["rules"]["max_depth"]["max_depth"] == 2  # yml beats pyproject


def test_pyproject_section_discovered(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(PYPROJECT_WITH_SECTION)

    config = ConfigResolver(cwd=tmp_path).resolve()
    assert config["rules"]["max_depth"]["max_depth"] == 4
    assert config["rules"]["max_depth"]["severity"] == "warning"


def test_defaults_when_nothing_found(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(PYPROJECT_WITHOUT_SECTION)

    config = ConfigResolver(cwd=tmp_path).resolve()
    assert config == DEFAULT_CONFIG
    assert config is not DEFAULT_CONFIG  # deep copy, caller can mutate safely


def test_invalid_severity_raises(tmp_path: Path) -> None:
    (tmp_path / "pybrace.yml").write_text(
        "rules:\n  max_depth:\n    enabled: true\n    severity: banana\n"
    )
    with pytest.raises(ConfigError, match="severity"):
        ConfigResolver(cwd=tmp_path).resolve()


def test_non_integer_threshold_raises(tmp_path: Path) -> None:
    (tmp_path / "pybrace.yml").write_text(
        "rules:\n  max_depth:\n    enabled: true\n    max_depth: deep\n"
    )
    with pytest.raises(ConfigError, match="max_depth"):
        ConfigResolver(cwd=tmp_path).resolve()


def test_non_bool_enabled_raises(tmp_path: Path) -> None:
    (tmp_path / "pybrace.yml").write_text(
        "rules:\n  max_depth:\n    enabled: yes please\n"
    )
    with pytest.raises(ConfigError, match="enabled"):
        ConfigResolver(cwd=tmp_path).resolve()


def test_invalid_toml_raises(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.pycleancode\nbroken")
    with pytest.raises(ConfigError, match="TOML"):
        ConfigResolver(cwd=tmp_path).resolve()
