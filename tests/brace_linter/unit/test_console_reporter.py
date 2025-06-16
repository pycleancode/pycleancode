from pycleancode.brace_linter.reports.models import NodeReport
from pycleancode.brace_linter.reports.console_reporter import ConsoleReporter


def test_console_reporter_print_tree(capsys):
    node = NodeReport(node_type="ROOT", start_line=0, depth=1)
    child = NodeReport(node_type="FunctionDef", start_line=1, depth=2)
    node.children.append(child)

    ConsoleReporter().print_tree(node)

    captured = capsys.readouterr()
    assert "ROOT" in captured.out
    assert "FunctionDef" in captured.out
