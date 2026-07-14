import textwrap

from pycleancode.brace_linter.analyzer import BraceLinterAnalyzer
from pycleancode.brace_linter.models import AnalysisRun

CONFIG = {
    "rules": {
        "max_depth": {"enabled": True, "max_depth": 3},
        "nested_function": {"enabled": True, "max_nested": 1, "severity": "warning"},
    }
}

NESTED_SOURCE = textwrap.dedent("""
    def outer():
        def inner():
            def too_deep():
                def more():
                    pass
    """)


def _write(tmp_path, name, content):
    target = tmp_path / name
    target.write_text(content)
    return str(target)


def test_analyze_returns_structured_run(tmp_path, capsys) -> None:
    source = _write(tmp_path, "sample.py", NESTED_SOURCE)
    run = BraceLinterAnalyzer().analyze(source, CONFIG, report=False)

    assert isinstance(run, AnalysisRun)
    assert run.files_analyzed == 1
    assert run.error_count > 0  # max_depth defaults to error
    assert run.warning_count > 0  # nested_function downgraded to warning
    assert run.results[0].structure is None
    assert run.results[0].summary.max_depth >= 4
    assert capsys.readouterr().out == ""  # analyzer no longer prints


def test_analyze_populates_structure_when_report_true(tmp_path) -> None:
    source = _write(tmp_path, "sample.py", NESTED_SOURCE)
    run = BraceLinterAnalyzer().analyze(source, CONFIG, report=True)
    assert run.results[0].structure is not None
    assert run.results[0].structure.node_type == "ROOT"


def test_analyze_records_parse_errors_and_continues(tmp_path) -> None:
    _write(tmp_path, "bad.py", "def broken(:\n")
    _write(tmp_path, "good.py", "def fine():\n    pass\n")
    run = BraceLinterAnalyzer().analyze(str(tmp_path), CONFIG, report=False)

    assert len(run.parse_errors) == 1
    assert "bad.py" in run.parse_errors[0]
    assert run.files_analyzed == 1  # good.py still analyzed
