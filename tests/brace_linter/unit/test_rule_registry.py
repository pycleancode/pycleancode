from pathlib import Path
from typing import List, Type, Generator

import pytest

from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.rules.registry import RuleRegistry
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation


# ✅ Fully typed dummy rule for test discovery
class DummyRule(RuleBase):
    @property
    def name(self) -> str:
        return "dummy"

    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        _ = vbt_root  # Access vbt_root to satisfy Pylance
        return []


@pytest.fixture
def temp_rule_package() -> Generator[Path, None, None]:
    """
    Create dummy rule directly inside real rules directory for test.
    """
    rules_dir = Path("pycleancode/brace_linter/rules")
    rule_file_path = rules_dir / "dummy_rule.py"

    # Write fake rule file
    rule_file_path.write_text(
        """
from pycleancode.brace_linter.rules.rule_base import RuleBase
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from pycleancode.brace_linter.rules.violation_model import RuleViolation
from typing import List

class DummyRule(RuleBase):
    @property
    def name(self) -> str:
        return "dummy"

    def run(self, vbt_root: VBTNode, file_path: str) -> List[RuleViolation]:
        _ = vbt_root
        return []
"""
    )

    yield rules_dir

    # Cleanup after test
    rule_file_path.unlink()


def test_discover_rules(temp_rule_package: Path) -> None:
    """
    Verify that RuleRegistry discovers rule classes correctly.
    """
    registry = RuleRegistry(rules_path=str(temp_rule_package))
    rules: List[Type[RuleBase]] = registry.discover_rules()

    rule_names = {rule.__name__ for rule in rules}
    assert "DummyRule" in rule_names
