import libcst as cst
from libcst.metadata import MetadataWrapper
from typing import List

from pycleancode.brace_linter.rules.max_depth_rule import MaxDepthRule
from pycleancode.brace_linter.rules.nested_function_rule import NestedFunctionRule
from pycleancode.brace_linter.rules.rule_engine import RuleEngine
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


def test_rule_engine_combined_rules() -> None:
    source_code = """
def my_func():
    def inner():
        def deeper():
            pass

    if True:
        for i in range(3):
            while i < 5:
                print(i)
"""
    vbt_root: VBTNode = build_vbt(source_code)

    rules = [MaxDepthRule(max_depth=3), NestedFunctionRule(max_nested=2)]

    engine = RuleEngine(rules)
    violations: List[RuleViolation] = engine.run(vbt_root, "dummy_file.py")

    assert len(violations) == 5

    violation_messages = [v.message for v in violations]
    assert any("Depth 4 exceeds max 3" in msg for msg in violation_messages)
    assert any("Depth 5 exceeds max 3" in msg for msg in violation_messages)
    assert any("Nested functions depth" in msg for msg in violation_messages)
