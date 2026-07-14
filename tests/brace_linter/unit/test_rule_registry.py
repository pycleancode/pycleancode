import types
from pathlib import Path
from typing import List

from pycleancode.brace_linter.rules.max_depth_rule import MaxDepthRule
from pycleancode.brace_linter.rules.nested_function_rule import NestedFunctionRule
from pycleancode.brace_linter.rules.registry import RuleRegistry
from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


def test_discover_rules_finds_builtin_rules() -> None:
    discovered = RuleRegistry().discover_rules()
    assert MaxDepthRule in discovered
    assert NestedFunctionRule in discovered
    assert all(issubclass(rule, RuleBase) for rule in discovered)


def test_list_rule_modules_filters_non_rule_files(tmp_path: Path) -> None:
    (tmp_path / "custom_rule.py").write_text("x = 1\n")
    (tmp_path / "__init__.py").write_text("")
    (tmp_path / "notes.txt").write_text("ignored")

    registry = RuleRegistry(rules_path=str(tmp_path))
    assert registry._list_rule_modules() == ["custom_rule"]


def test_extract_rule_classes_ignores_non_rule_members() -> None:
    class FakeRule(RuleBase):
        @property
        def name(self) -> str:
            return "fake"

        def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
            return []

    module = types.ModuleType("fake_rules_module")
    module.FakeRule = FakeRule  # type: ignore[attr-defined]
    module.Unrelated = dict  # type: ignore[attr-defined]

    extracted = RuleRegistry()._extract_rule_classes(module)
    assert extracted == [FakeRule]
