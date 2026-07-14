"""
Module: console_reporter

Prints NodeReport tree structures to console using Rich.
"""

from typing import Optional

from rich.console import Console

from pycleancode.brace_linter.reports.models import NodeReport


class ConsoleReporter:
    """
    ConsoleReporter prints NodeReport trees with icons and colors.
    """

    def __init__(self, console: Optional[Console] = None) -> None:
        """
        Initialize ConsoleReporter.

        Args:
            console (Optional[Console]): Rich console to print to.
                Defaults to a stdout console.
        """
        self._console = console or Console()

    def print_tree(self, report: NodeReport, prefix: str = "") -> None:
        """
        Recursively print NodeReport tree.

        Args:
            report (NodeReport): The node to print.
            prefix (str): Prefix for tree indentation.
        """
        self._print_node(report, prefix)

        for index, child in enumerate(report.children):
            new_prefix = self._calculate_prefix(prefix, index, len(report.children))
            self.print_tree(child, new_prefix)

    def _print_node(self, report: NodeReport, prefix: str) -> None:
        icon = self._get_icon(report.node_type)
        color = self._get_color(report.depth)
        connector = prefix[:-2].replace(" ", "│ ") + ("├─" if prefix else "")
        self._console.print(
            f"[{color}]{connector} {icon} {report.node_type} (Line {report.start_line}, Depth {report.depth})[/{color}]"
        )

    def _calculate_prefix(self, prefix: str, index: int, total: int) -> str:
        return prefix + ("   " if index == total - 1 else "│  ")

    def _get_icon(self, node_type: str) -> str:
        icon_map = {
            "ROOT": "🟦",
            "FunctionDef": "🔷",
            "If": "🔸",
        }
        return icon_map.get(node_type, "▪️")

    def _get_color(self, depth: int) -> str:
        if depth <= 2:
            return "cyan"
        if depth <= 4:
            return "green"
        if depth <= 6:
            return "yellow"
        return "red"
