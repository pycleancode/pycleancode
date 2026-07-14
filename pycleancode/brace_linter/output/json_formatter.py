"""
Module: output.json_formatter

Renders AnalysisRun as machine-readable JSON (schemaVersion 1).
"""

import json
from typing import Any, Dict, List

from pycleancode.brace_linter.models import AnalysisRun

SCHEMA_VERSION = 1


class JsonFormatter:
    """
    JsonFormatter renders results as a stable, versioned JSON document.
    """

    def render(self, run: AnalysisRun) -> str:
        """
        Render the analysis run as JSON.

        Args:
            run (AnalysisRun): Structured analysis results.

        Returns:
            str: JSON document terminated by a newline.
        """
        violations: List[Dict[str, Any]] = [
            {
                "file": violation.file_path,
                "line": violation.line_number,
                "rule": violation.rule_name,
                "severity": violation.severity,
                "message": violation.message,
            }
            for result in run.results
            for violation in result.violations
        ]
        violations.sort(key=lambda item: (item["file"], item["line"]))

        files: List[Dict[str, Any]] = [
            {
                "path": result.file_path,
                "maxDepth": result.summary.max_depth,
                "nestedFunctionDepth": result.summary.nested_function_depth,
                "violations": len(result.violations),
            }
            for result in run.results
        ]

        payload: Dict[str, Any] = {
            "schemaVersion": SCHEMA_VERSION,
            "summary": {
                "files": run.files_analyzed,
                "errors": run.error_count,
                "warnings": run.warning_count,
            },
            "files": files,
            "parseErrors": list(run.parse_errors),
            "violations": violations,
        }
        return json.dumps(payload, indent=2) + "\n"
