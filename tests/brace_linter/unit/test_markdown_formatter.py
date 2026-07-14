from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.output.markdown_formatter import MarkdownFormatter
from pycleancode.brace_linter.reports.models import FileSummary
from pycleancode.brace_linter.rules.violation_model import RuleViolation


def _run() -> AnalysisRun:
    violation = RuleViolation(
        file_path="src/a.py",
        line_number=5,
        message="Depth 4 exceeds max 3",
        rule_name="max_depth",
        severity="error",
    )
    summary = FileSummary(
        file_path="src/a.py", max_depth=4, nested_function_depth=0, total_violations=1
    )
    return AnalysisRun(
        results=[
            FileResult(file_path="src/a.py", violations=[violation], summary=summary)
        ]
    )


def test_markdown_document_shape() -> None:
    rendered = MarkdownFormatter().render(_run())
    assert rendered.startswith("# PyCleanCode Report\n")
    assert "**Files analyzed:** 1 · **Errors:** 1 · **Warnings:** 0" in rendered
    assert "| File | Line | Rule | Severity | Message |" in rendered
    assert "| src/a.py | 5 | max_depth | error | Depth 4 exceeds max 3 |" in rendered


def test_markdown_clean_run_message() -> None:
    rendered = MarkdownFormatter().render(AnalysisRun())
    assert "No violations found." in rendered
    assert "| File |" not in rendered


def test_markdown_parse_errors_section() -> None:
    run = AnalysisRun(parse_errors=["bad.py: Syntax Error"])
    rendered = MarkdownFormatter().render(run)
    assert "## Parse Errors" in rendered
    assert "- bad.py: Syntax Error" in rendered
