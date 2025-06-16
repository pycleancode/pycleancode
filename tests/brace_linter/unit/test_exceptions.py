import pytest
from pycleancode.brace_linter.exceptions.errors import (
    BraceLinterError,
    ConfigError,
    ParserError,
)


def test_exceptions_inheritance():
    assert issubclass(ConfigError, BraceLinterError)
    assert issubclass(ParserError, BraceLinterError)


def test_exceptions_raised():
    with pytest.raises(ConfigError):
        raise ConfigError("Config error")

    with pytest.raises(ParserError):
        raise ParserError("Parser error")
