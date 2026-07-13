from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.reports.models import FileSummary
from pycleancode.brace_linter.rules.violation_model import RuleViolation


def _result(file_path: str, severities: list) -> FileResult:
    violations = [
        RuleViolation(
            file_path=file_path,
            line_number=index + 1,
            message="msg",
            rule_name="max_depth",
            severity=severity,
        )
        for index, severity in enumerate(severities)
    ]
    summary = FileSummary(
        file_path=file_path,
        max_depth=4,
        nested_function_depth=2,
        total_violations=len(violations),
    )
    return FileResult(file_path=file_path, violations=violations, summary=summary)


def test_empty_run_counts() -> None:
    run = AnalysisRun()
    assert run.files_analyzed == 0
    assert run.error_count == 0
    assert run.warning_count == 0
    assert run.parse_errors == []


def test_counts_across_files() -> None:
    run = AnalysisRun(
        results=[_result("a.py", ["error", "warning"]), _result("b.py", ["error"])]
    )
    assert run.files_analyzed == 2
    assert run.error_count == 2
    assert run.warning_count == 1


def test_structure_defaults_to_none() -> None:
    result = _result("a.py", [])
    assert result.structure is None
