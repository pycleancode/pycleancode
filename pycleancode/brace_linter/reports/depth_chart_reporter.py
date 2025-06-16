"""
Module: depth_chart_reporter

Prints a simple depth chart for source file analysis.
"""

from rich import print


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
        print(f"{file_path} | Max Depth: {max_depth} | {chart}")

    def _generate_bar(self, depth: int) -> str:
        """
        Generate the bar chart string based on depth.

        Args:
            depth (int): The depth value.

        Returns:
            str: The generated chart.
        """
        return "▓" * depth
