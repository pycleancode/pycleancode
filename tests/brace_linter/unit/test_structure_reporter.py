from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.reports.structure_reporter import StructureReporter
from pycleancode.brace_linter.reports.models import NodeReport


def test_structure_reporter_build_report() -> None:
    # Create dummy VBT tree
    vbt_root = VBTNode(node_type="ROOT", start_line=0, end_line=0)
    func_node = VBTNode(node_type="FunctionDef", start_line=1, end_line=10)
    if_node = VBTNode(node_type="If", start_line=2, end_line=5)

    vbt_root.add_child(func_node)
    func_node.add_child(if_node)

    # Run structure reporter
    reporter = StructureReporter()
    report: NodeReport = reporter.build_report(vbt_root)

    # Validate report tree structure
    assert report.node_type == "ROOT"
    assert report.start_line == 0
    assert report.depth == 1

    assert len(report.children) == 1
    child_func = report.children[0]
    assert child_func.node_type == "FunctionDef"
    assert child_func.depth == 2

    child_if = child_func.children[0]
    assert child_if.node_type == "If"
    assert child_if.depth == 3
