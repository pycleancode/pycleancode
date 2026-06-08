"""
Module: console

Provides helpers for safe console output.
"""

import re
from typing import Any

_CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def sanitize_console_text(value: Any) -> str:
    """
    Escape control characters before writing untrusted text to the console.
    """
    return _CONTROL_CHAR_PATTERN.sub(
        lambda match: f"\\x{ord(match.group(0)):02x}", str(value)
    )
