import libcst as cst
from libcst.metadata import MetadataWrapper
from typing import List

from pycleancode.brace_linter.rules.max_depth_rule import MaxDepthRule
from pycleancode.brace_linter.vbtree.vbt_builder import VBTBuilder
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation


def build_vbt(source_code: str) -> VBTNode:
    """
    Utility helper to parse source code into VBTNode.
    """
    tree = cst.parse_module(source_code)
    wrapper = MetadataWrapper(tree)
    builder = VBTBuilder(wrapper)
    return builder.build()


def test_max_depth_no_violation() -> None:
    source_code = """
def my_func():
    if True:
        for i in range(3):
            print(i)
"""
    vbt_root: VBTNode = build_vbt(source_code)

    # ✅ Max depth = 4 (ROOT=1, FunctionDef=2, If=3, For=4)
    rule = MaxDepthRule(max_depth=4)

    violations: List[RuleViolation] = rule.run(vbt_root, "dummy_file.py")
    assert violations == []


def test_max_depth_violation_detected() -> None:
    source_code = """
def my_func():
    if True:
        for i in range(3):
            while i < 5:
                if i > 0:
                    print(i)
"""
    vbt_root: VBTNode = build_vbt(source_code)
    rule = MaxDepthRule(max_depth=3)
    violations: List[RuleViolation] = rule.run(vbt_root, "dummy_file.py")

    # ✅ Violations triggered at For (depth=4), While (depth=5), If (depth=6)
    assert len(violations) == 3

    violation_lines = {v.line_number for v in violations}
    assert violation_lines == {4, 5, 6}

    for v in violations:
        assert "Depth" in v.message
