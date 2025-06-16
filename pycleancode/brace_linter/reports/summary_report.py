"""
Module: summary_reporter

Generates summary statistics from NodeReport trees.
"""

from pycleancode.brace_linter.reports.models import NodeReport, FileSummary


class SummaryReporter:
    """
    SummaryReporter generates summary statistics from NodeReport trees.
    """

    def generate_summary(
        self, file_path: str, report: NodeReport, total_violations: int
    ) -> FileSummary:
        """
        Generate FileSummary from a NodeReport tree.

        Args:
            file_path (str): File path being summarized.
            report (NodeReport): The full node report tree.
            total_violations (int): Total violations found.

        Returns:
            FileSummary: Summary report.
        """
        max_depth = self._calculate_max_depth(report)
        nested_fn_depth = self._calculate_nested_function_depth(report)
        return FileSummary(file_path, max_depth, nested_fn_depth, total_violations)

    def _calculate_max_depth(self, node: NodeReport) -> int:
        """
        Recursively calculate maximum depth.
        """
        if not node.children:
            return node.depth

        child_depths = (self._calculate_max_depth(child) for child in node.children)
        return max(child_depths)

    def _calculate_nested_function_depth(self, node: NodeReport) -> int:
        """
        Recursively calculate maximum nested function depth.
        """
        current_depth = node.depth if node.node_type == "FunctionDef" else 0

        child_depths = (
            self._calculate_nested_function_depth(child) for child in node.children
        )

        return max([current_depth, *child_depths])
