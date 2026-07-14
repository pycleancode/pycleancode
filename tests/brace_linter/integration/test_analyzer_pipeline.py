import pytest
from pycleancode.brace_linter.analyzer import BraceLinterAnalyzer


@pytest.fixture
def sample_file(tmp_path):
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


def test_analyzer_pipeline_runs(sample_file):
    config = {
        "rules": {
            "max_depth": {"enabled": True, "max_depth": 3},
            "nested_function": {"enabled": True, "max_nested": 1},
        }
    }
    run = BraceLinterAnalyzer().analyze(sample_file, config, report=False)

    assert run.files_analyzed == 1
    assert run.error_count > 0
    messages = [v.message for r in run.results for v in r.violations]
    assert any("Depth" in m for m in messages)
