"""
Module: analyzer

Main orchestration class for pycleancode analysis pipeline.
"""

import libcst as cst
from libcst.metadata import MetadataWrapper
from pycleancode.brace_linter.vbtree.vbt_builder import VBTBuilder
from pycleancode.brace_linter.filesystem.file_loader import FileLoader
from pycleancode.brace_linter.rules.loader import RuleLoader
from pycleancode.brace_linter.rules.rule_engine import RuleEngine
from pycleancode.brace_linter.reports.structure_reporter import StructureReporter
from pycleancode.brace_linter.reports.console_reporter import ConsoleReporter
from pycleancode.brace_linter.reports.summary_report import SummaryReporter
from pycleancode.brace_linter.reports.depth_chart_reporter import DepthChartReporter
from core.config import ConfigLoader
from typing import List
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation


class BraceLinterAnalyzer:
    """
    Coordinates full analysis pipeline: parsing, rule evaluation, and reporting.
    """

    def analyze(self, path: str, config_path: str, report: bool) -> None:
        config = ConfigLoader().load(config_path)
        files = FileLoader().load_files(path)
        rules = RuleLoader(config).load_rules()

        for file_path, file_content in files.items():
            print(f"\n🔎 Analyzing: {file_path}")
            vbt_root: VBTNode = self._parse_to_vbt(file_content)
            violations = RuleEngine(rules).run(vbt_root, file_path)

            self._print_violations(violations)

            if report:
                self._generate_report(file_path, vbt_root, violations)

    def _parse_to_vbt(self, file_content: str) -> VBTNode:
        tree = cst.parse_module(file_content)
        wrapper = MetadataWrapper(tree)
        vbt_root: VBTNode = VBTBuilder(wrapper).build()
        return vbt_root

    def _print_violations(self, violations: List[RuleViolation]) -> None:
        for violation in violations:
            print(f"{violation.file_path}:{violation.line_number}: {violation.message}")

    def _generate_report(
        self, file_path: str, vbt_root: VBTNode, violations: list[RuleViolation]
    ) -> None:
        print("\n📊 Structural Report:\n")
        report_tree = StructureReporter().build_report(vbt_root)
        ConsoleReporter().print_tree(report_tree)

        summary = SummaryReporter().generate_summary(
            file_path, report_tree, len(violations)
        )

        print("\n📈 Summary:")
        print(f"- 🧮 Max Depth: {summary.max_depth}")
        print(f"- 🧬 Nested Functions Depth: {summary.nested_function_depth}")
        print(f"- 🚫 Total Violations: {summary.total_violations}")

        DepthChartReporter().print_chart(file_path, summary.max_depth)
