from pycleancode.brace_linter.rules.loader import RuleLoader
from pycleancode.brace_linter.rules.max_depth_rule import MaxDepthRule


def _config(severity_value: str) -> dict:
    return {
        "rules": {
            "max_depth": {"enabled": True, "max_depth": 2, "severity": severity_value},
            "nested_function": {"enabled": True, "max_nested": 1},
        }
    }


def test_severities_default_to_error() -> None:
    loader = RuleLoader(_config("warning"))
    loader.load_rules()
    assert loader.severities == {"max_depth": "warning", "nested_function": "error"}


def test_severity_key_not_passed_to_constructor() -> None:
    loader = RuleLoader(_config("warning"))
    rules = loader.load_rules()
    max_depth_rule = next(r for r in rules if r.name == "max_depth")
    # threshold must survive: severity/enabled were stripped, max_depth passed through
    assert isinstance(max_depth_rule, MaxDepthRule)
    assert max_depth_rule._max_depth == 2


def test_severities_empty_before_load() -> None:
    loader = RuleLoader(_config("error"))
    assert loader.severities == {}
