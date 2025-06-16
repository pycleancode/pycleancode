from pycleancode.brace_linter.reports.summary_report import SummaryReporter
from pycleancode.brace_linter.reports.depth_chart_reporter import DepthChartReporter
from pycleancode.brace_linter.reports.models import NodeReport
from pycleancode.brace_linter.reports.models import FileSummary


def build_sample_report() -> NodeReport:
    # Build mock structure like:
    #
    # ROOT
    # ├── FunctionDef (depth=2)
    # │   └── If (depth=3)
    # │        └── For (depth=4)
    func_node = NodeReport(node_type="FunctionDef", start_line=1, depth=2)
    if_node = NodeReport(node_type="If", start_line=2, depth=3)
    for_node = NodeReport(node_type="For", start_line=3, depth=4)

    if_node.children.append(for_node)
    func_node.children.append(if_node)

    root = NodeReport(node_type="ROOT", start_line=0, depth=1)
    root.children.append(func_node)

    return root


def test_summary_reporter_generate_summary() -> None:
    vbt_root = build_sample_report()
    reporter = SummaryReporter()

    summary: FileSummary = reporter.generate_summary(
        file_path="dummy_file.py", report=vbt_root, total_violations=3
    )

    assert summary.file_path == "dummy_file.py"
    assert summary.max_depth == 4
    assert summary.nested_function_depth == 2
    assert summary.total_violations == 3


def test_depth_chart_reporter_output(capsys) -> None:
    reporter = DepthChartReporter()
    reporter.print_chart("dummy_file.py", max_depth=5)

    captured = capsys.readouterr()
    assert "dummy_file.py | Max Depth: 5 | ▓▓▓▓▓" in captured.out
