import pytest
from pycleancode.brace_linter.rules.rule_base import RuleBase


def test_rule_base_interface_not_instantiable():
    with pytest.raises(TypeError):
        RuleBase()
