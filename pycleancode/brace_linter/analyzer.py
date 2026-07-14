"""
Module: analyzer

Main orchestration class for pycleancode analysis pipeline.
"""

from typing import Any, Dict

import libcst as cst
from libcst.metadata import MetadataWrapper

from pycleancode.brace_linter.filesystem.file_loader import FileLoader
from pycleancode.brace_linter.models import AnalysisRun, FileResult
from pycleancode.brace_linter.reports.structure_reporter import StructureReporter
from pycleancode.brace_linter.reports.summary_report import SummaryReporter
from pycleancode.brace_linter.rules.loader import RuleLoader
from pycleancode.brace_linter.rules.rule_engine import RuleEngine
from pycleancode.brace_linter.vbtree.vbt_builder import VBTBuilder
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


class BraceLinterAnalyzer:
    """
    Coordinates the analysis pipeline: parsing, rule evaluation, and
    result aggregation. Produces data only; rendering is the output
    layer's job.
    """

    def analyze(
        self, path: str, config: Dict[str, Any], report: bool = False
    ) -> AnalysisRun:
        """
        Analyze a file or directory and return structured results.

        Args:
            path (str): File or directory to analyze.
            config (Dict[str, Any]): Resolved rule configuration.
            report (bool): Attach structural NodeReport trees to results.

        Returns:
            AnalysisRun: Aggregated results including per-file violations,
            summaries, and any parse errors.
        """
        files = FileLoader().load_files(path)
        loader = RuleLoader(config)
        rules = loader.load_rules()
        engine = RuleEngine(rules, loader.severities)

        run = AnalysisRun()

        for file_path, file_content in files.items():
            try:
                vbt_root = self._parse_to_vbt(file_content)
            except cst.ParserSyntaxError as exc:
                first_line = str(exc).splitlines()[0]
                run.parse_errors.append(f"{file_path}: {first_line}")
                continue

            violations = engine.run(vbt_root, file_path)
            tree = StructureReporter().build_report(vbt_root)
            summary = SummaryReporter().generate_summary(
                file_path, tree, len(violations)
            )
            run.results.append(
                FileResult(
                    file_path=file_path,
                    violations=violations,
                    summary=summary,
                    structure=tree if report else None,
                )
            )

        return run

    def _parse_to_vbt(self, file_content: str) -> VBTNode:
        tree = cst.parse_module(file_content)
        wrapper = MetadataWrapper(tree)
        vbt_root: VBTNode = VBTBuilder(wrapper).build()
        return vbt_root
