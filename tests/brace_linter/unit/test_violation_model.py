from pycleancode.brace_linter.rules.violation_model import (
    DEFAULT_SEVERITY,
    VALID_SEVERITIES,
    RuleViolation,
)


def test_violation_defaults_to_error_severity() -> None:
    violation = RuleViolation(
        file_path="a.py", line_number=3, message="Depth 4 exceeds max 3"
    )
    assert violation.severity == "error"
    assert violation.rule_name == ""


def test_violation_accepts_explicit_rule_and_severity() -> None:
    violation = RuleViolation(
        file_path="a.py",
        line_number=3,
        message="msg",
        rule_name="max_depth",
        severity="warning",
    )
    assert violation.rule_name == "max_depth"
    assert violation.severity == "warning"


def test_violation_str_format_is_unchanged() -> None:
    violation = RuleViolation(file_path="a.py", line_number=3, message="msg")
    assert str(violation) == "a.py:3: msg"


def test_severity_constants() -> None:
    assert DEFAULT_SEVERITY == "error"
    assert VALID_SEVERITIES == ("error", "warning")
