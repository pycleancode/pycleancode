"""
Module: structure_reporter

Converts VBTNode trees into NodeReport trees for reporting.
"""

from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.reports.models import NodeReport


class StructureReporter:
    """
    StructureReporter builds NodeReport trees from VBTNode trees.
    """

    def build_report(self, vbt_root: VBTNode) -> NodeReport:
        """
        Build a NodeReport tree from a VBTNode tree.

        Args:
            vbt_root (VBTNode): Root node of parsed VBT tree.

        Returns:
            NodeReport: Root of the generated report tree.
        """
        return self._visit_node(vbt_root, depth=1)

    def _visit_node(self, node: VBTNode, depth: int) -> NodeReport:
        """
        Visit a node and recursively build report tree.

        Args:
            node (VBTNode): Current VBT node.
            depth (int): Current depth.

        Returns:
            NodeReport: Generated report node.
        """
        report_node = NodeReport(
            node_type=node.node_type,
            start_line=node.start_line,
            depth=depth,
        )

        report_node.children = [
            self._visit_node(child, depth + 1) for child in node.children
        ]

        return report_node
