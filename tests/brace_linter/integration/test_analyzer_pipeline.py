import pytest
from pycleancode.brace_linter.analyzer import BraceLinterAnalyzer


@pytest.fixture
def sample_file(tmp_path):
    # Create a temporary sample test file
    content = """
def outer():
    def inner():
        def too_deep():
            def more():
                pass
"""
    file_path = tmp_path / "sample_nested.py"
    file_path.write_text(content)
    return str(file_path)


@pytest.fixture
def config_file(tmp_path):
    # Create a temporary config file
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
    return str(config_path)


def test_analyzer_pipeline_runs(sample_file, config_file):
    analyzer = BraceLinterAnalyzer()
    # We're running with report=False to avoid console output during test
    analyzer.analyze(sample_file, config_file, report=False)

    # If no exceptions occur -> we assume pipeline ran successfully
    # (Later you can expand this with mock or capture actual violations)
