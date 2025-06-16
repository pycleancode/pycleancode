"""
Module: exceptions

Defines custom exception hierarchy for the BraceLinter application.
"""


class BraceLinterError(Exception):
    """
    Base exception class for all BraceLinter-related errors.
    """


class ConfigError(BraceLinterError):
    """
    Raised when there is a configuration-related error.
    """


class ParserError(BraceLinterError):
    """
    Raised when there is a parsing-related error.
    """
