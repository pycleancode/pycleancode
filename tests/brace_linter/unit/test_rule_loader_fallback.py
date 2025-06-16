from pycleancode.brace_linter.rules.loader import RuleLoader


class DummyRule:
    name = "dummy"


def test_rule_loader_instantiates_rule():
    # Simulate discovered rule classes manually
    loader = RuleLoader(config={"rules": {"dummy": {"enabled": True}}})
    loader.registry.discover_rules = lambda: [DummyRule]  # monkeypatch registry

    rules = loader.load_rules()

    assert len(rules) == 1
    assert isinstance(rules[0], DummyRule)
