import json

from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.output.json_formatter import JsonFormatter
from pycleancode.brace_linter.reports.models import FileSummary
from pycleancode.brace_linter.rules.violation_model import RuleViolation


def _result(file_path: str, line: int, severity: str) -> FileResult:
    violation = RuleViolation(
        file_path=file_path,
        line_number=line,
        message="msg",
        rule_name="max_depth",
        severity=severity,
    )
    summary = FileSummary(
        file_path=file_path, max_depth=4, nested_function_depth=0, total_violations=1
    )
    return FileResult(file_path=file_path, violations=[violation], summary=summary)


def test_json_schema_shape() -> None:
    run = AnalysisRun(
        results=[_result("b.py", 9, "warning"), _result("a.py", 5, "error")],
        parse_errors=["bad.py: Syntax Error"],
    )
    payload = json.loads(JsonFormatter().render(run))

    assert payload["schemaVersion"] == 1
    assert payload["summary"] == {"files": 2, "errors": 1, "warnings": 1}
    assert payload["files"] == [
        {"path": "b.py", "maxDepth": 4, "nestedFunctionDepth": 0, "violations": 1},
        {"path": "a.py", "maxDepth": 4, "nestedFunctionDepth": 0, "violations": 1},
    ]
    assert payload["parseErrors"] == ["bad.py: Syntax Error"]
    assert payload["violations"] == [
        {
            "file": "a.py",
            "line": 5,
            "rule": "max_depth",
            "severity": "error",
            "message": "msg",
        },
        {
            "file": "b.py",
            "line": 9,
            "rule": "max_depth",
            "severity": "warning",
            "message": "msg",
        },
    ]


def test_json_empty_run() -> None:
    payload = json.loads(JsonFormatter().render(AnalysisRun()))
    assert payload["summary"] == {"files": 0, "errors": 0, "warnings": 0}
    assert payload["files"] == []
    assert payload["violations"] == []
    assert payload["parseErrors"] == []


def test_json_ends_with_newline() -> None:
    assert JsonFormatter().render(AnalysisRun()).endswith("\n")
