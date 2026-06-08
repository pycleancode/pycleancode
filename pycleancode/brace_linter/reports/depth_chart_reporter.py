"""
Module: depth_chart_reporter

Prints a simple depth chart for source file analysis.
"""

from rich import print
from pycleancode.utils.console import sanitize_console_text


class DepthChartReporter:
    """
    DepthChartReporter prints max depth analysis using a simple bar chart.
    """

    def print_chart(self, file_path: str, max_depth: int) -> None:
        """
        Print the depth chart for a given file.

        Args:
            file_path (str): Path of the file being analyzed.
            max_depth (int): Maximum depth found.
        """
        chart = self._generate_bar(max_depth)
        safe_file_path = sanitize_console_text(file_path)
        print(f"{safe_file_path} | Max Depth: {max_depth} | {chart}")

    def _generate_bar(self, depth: int) -> str:
        """
        Generate the bar chart string based on depth.

        Args:
            depth (int): The depth value.

        Returns:
            str: The generated chart.
        """
        return "▓" * depth
