import subprocess
import pytest


@pytest.fixture
def sample_python_file(tmp_path):
    content = """
def outer():
    def inner():
        def too_deep():
            def more():
                pass
"""
    file_path = tmp_path / "sample_nested.py"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_config_file(tmp_path):
    content = """
rules:
  max_depth:
    enabled: true
    max_depth: 3
  nested_function:
    enabled: true
    max_nested: 1
"""
    config_path = tmp_path / "pybrace.yml"
    config_path.write_text(content)
    return config_path


def test_cli_pipeline_runs(sample_python_file, sample_config_file):
    # We execute the actual CLI binary installed by poetry
    cmd = [
        "poetry",
        "run",
        "pycleancode-brace-linter",
        str(sample_python_file),
        "--config",
        str(sample_config_file),
        "--report",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check exit code
    assert result.returncode == 0

    # Check expected violation keywords in output
    assert "Nested functions depth" in result.stdout
    assert "Depth" in result.stdout
    assert "Max Depth" in result.stdout
