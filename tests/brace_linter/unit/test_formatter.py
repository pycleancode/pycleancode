from typing import List
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.brace_linter.reporter.formatter import Formatter


def test_formatter_prints_violations(capsys) -> None:
    violations = [
        RuleViolation(
            file_path="file1.py", line_number=10, message="Depth 4 exceeds max 3"
        ),
        RuleViolation(
            file_path="file2.py",
            line_number=5,
            message="Nested functions depth 3 exceeds allowed 2",
        ),
    ]

    Formatter.format(violations)

    captured = capsys.readouterr()

    assert "file1.py:10: Depth 4 exceeds max 3" in captured.out
    assert "file2.py:5: Nested functions depth 3 exceeds allowed 2" in captured.out


def test_formatter_empty_list(capsys) -> None:
    violations: List[RuleViolation] = []
    Formatter.format(violations)

    captured = capsys.readouterr()
    assert captured.out == ""
