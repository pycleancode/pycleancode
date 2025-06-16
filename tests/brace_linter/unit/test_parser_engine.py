import os
import tempfile
import pytest
import libcst as cst
from libcst.metadata import MetadataWrapper

from pycleancode.brace_linter.parser.parser_engine import ParserEngine


@pytest.fixture
def parser_engine() -> ParserEngine:
    return ParserEngine()


def test_parse_valid_file(parser_engine: ParserEngine) -> None:
    source_code = """
def my_func():
    print("Hello")
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(source_code)
        temp_file_path = temp_file.name

    try:
        parsed_cst, wrapper = parser_engine.parse(temp_file_path)

        assert isinstance(parsed_cst, cst.Module)
        assert isinstance(wrapper, MetadataWrapper)

        # Check that CST parsing succeeded:
        func_defs = [n for n in parsed_cst.body if isinstance(n, cst.FunctionDef)]
        assert len(func_defs) == 1
        assert func_defs[0].name.value == "my_func"
    finally:
        os.remove(temp_file_path)


def test_parse_file_not_found(parser_engine: ParserEngine) -> None:
    with pytest.raises(OSError):
        parser_engine.parse("non_existent_file.py")
