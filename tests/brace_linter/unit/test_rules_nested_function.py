import libcst as cst
from libcst.metadata import MetadataWrapper
from typing import List

from pycleancode.brace_linter.rules.nested_function_rule import NestedFunctionRule
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


def test_nested_function_no_violation() -> None:
    source_code = """
def my_func():
    pass
"""
    vbt_root: VBTNode = build_vbt(source_code)
    rule = NestedFunctionRule(max_nested=1)
    violations: List[RuleViolation] = rule.run(vbt_root, "dummy_file.py")

    assert violations == []


def test_nested_function_one_nested_allowed() -> None:
    source_code = """
def my_func():
    def inner():
        pass
"""
    vbt_root: VBTNode = build_vbt(source_code)
    rule = NestedFunctionRule(max_nested=2)
    violations: List[RuleViolation] = rule.run(vbt_root, "dummy_file.py")

    assert violations == []


def test_nested_function_violation_detected() -> None:
    source_code = """
def my_func():
    def inner():
        def deeper():
            def deepest():
                pass
"""
    vbt_root: VBTNode = build_vbt(source_code)
    rule = NestedFunctionRule(max_nested=2)
    violations: List[RuleViolation] = rule.run(vbt_root, "dummy_file.py")

    assert len(violations) == 2
    violation_lines = {v.line_number for v in violations}
    assert violation_lines == {4, 5}
