from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.output.text_formatter import TextFormatter
from pycleancode.brace_linter.reports.models import FileSummary, NodeReport
from pycleancode.brace_linter.rules.violation_model import RuleViolation


def _run(with_structure: bool = False) -> AnalysisRun:
    violation = RuleViolation(
        file_path="src/a.py",
        line_number=5,
        message="Depth 4 exceeds max 3",
        rule_name="max_depth",
        severity="error",
    )
    summary = FileSummary(
        file_path="src/a.py", max_depth=4, nested_function_depth=2, total_violations=1
    )
    structure = None
    if with_structure:
        structure = NodeReport(node_type="ROOT", start_line=0, depth=1)
    result = FileResult(
        file_path="src/a.py",
        violations=[violation],
        summary=summary,
        structure=structure,
    )
    return AnalysisRun(results=[result])


def test_text_contains_header_and_violation_line() -> None:
    rendered = TextFormatter().render(_run())
    assert "🔎 Analyzing: src/a.py" in rendered
    assert "src/a.py:5: Depth 4 exceeds max 3" in rendered
    assert "Structural Report" not in rendered  # no structure attached


def test_text_renders_report_sections_when_structure_present() -> None:
    rendered = TextFormatter().render(_run(with_structure=True))
    assert "📊 Structural Report:" in rendered
    assert "ROOT (Line 0, Depth 1)" in rendered
    assert "📈 Summary:" in rendered
    assert "- 🧮 Max Depth: 4" in rendered
    assert "- 🧬 Nested Functions Depth: 2" in rendered
    assert "- 🚫 Total Violations: 1" in rendered
    assert "Max Depth: 4 | ▓▓▓▓" in rendered


def test_text_lists_parse_errors() -> None:
    run = AnalysisRun(parse_errors=["src/bad.py: Syntax Error @ 1:1."])
    rendered = TextFormatter().render(run)
    assert "error: could not parse src/bad.py" in rendered


def test_text_sanitizes_control_characters() -> None:
    run = _run()
    run.results[0].violations[0].message = "evil\x1b[31mmsg"
    rendered = TextFormatter().render(run)
    assert "\x1b" not in rendered
    assert "\\x1b" in rendered
