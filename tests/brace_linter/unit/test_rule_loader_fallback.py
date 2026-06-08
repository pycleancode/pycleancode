from pycleancode.brace_linter.rules.loader import RuleLoader
from pycleancode.brace_linter.rules.max_depth_rule import MaxDepthRule
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


class DummyRule:
    name = "dummy"


def test_rule_loader_instantiates_rule():
    # Simulate discovered rule classes manually
    loader = RuleLoader(config={"rules": {"dummy": {"enabled": True}}})
    loader.registry.discover_rules = lambda: [DummyRule]  # monkeypatch registry

    rules = loader.load_rules()

    assert len(rules) == 1
    assert isinstance(rules[0], DummyRule)


def test_rule_loader_preserves_rule_threshold_from_config():
    loader = RuleLoader(
        config={"rules": {"max_depth": {"enabled": True, "max_depth": 1}}}
    )
    loader.registry.discover_rules = lambda: [MaxDepthRule]  # monkeypatch registry

    rules = loader.load_rules()

    root = VBTNode(node_type="ROOT", start_line=0, end_line=0)
    root.add_child(VBTNode(node_type="FunctionDef", start_line=1, end_line=1))
    violations = rules[0].run(root, "sample.py")

    assert len(rules) == 1
    assert len(violations) == 1
    assert "Depth 2 exceeds max 1" in violations[0].message
