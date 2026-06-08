from pycleancode.brace_linter.reports.depth_chart_reporter import DepthChartReporter
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.brace_linter.reporter.formatter import Formatter
from pycleancode.utils.console import sanitize_console_text


def test_sanitize_console_text_escapes_control_characters() -> None:
    unsafe_path = "sample\x1b[31m\nfile.py"

    assert sanitize_console_text(unsafe_path) == "sample\\x1b[31m\\x0afile.py"


def test_formatter_sanitizes_violation_output(capsys) -> None:
    violation = RuleViolation(
        file_path="sample\x1b[31m.py",
        line_number=1,
        message="Depth 2 exceeds max 1",
    )

    Formatter.format([violation])

    output = capsys.readouterr().out
    assert "\x1b" not in output
    assert "sample\\x1b[31m.py:1: Depth 2 exceeds max 1" in output


def test_depth_chart_reporter_sanitizes_file_path(capsys) -> None:
    DepthChartReporter().print_chart("sample\x1b[31m.py", 2)

    output = capsys.readouterr().out
    assert "\x1b" not in output
    assert "sample\\x1b[31m.py | Max Depth: 2" in output
