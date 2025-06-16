"""
Module: parser_engine

Provides ParserEngine for parsing Python files into CST using libcst.
"""

from typing import Tuple
from libcst import parse_module, MetadataWrapper, Module


class ParserEngine:
    """
    ParserEngine parses Python files into Concrete Syntax Trees (CST) using libcst.
    """

    def parse(
        self, file_path: str, encoding: str = "utf-8"
    ) -> Tuple[Module, MetadataWrapper]:
        """
        Parse the given Python file and return the CST and its metadata wrapper.

        Args:
            file_path (str): Path to the Python file to parse.
            encoding (str): File encoding. Default is utf-8.

        Returns:
            Tuple[Module, MetadataWrapper]: Parsed CST and metadata wrapper.
        """
        source = self._read_file(file_path, encoding)
        cst = parse_module(source)
        wrapper = MetadataWrapper(cst)
        return cst, wrapper

    def _read_file(self, file_path: str, encoding: str) -> str:
        """
        Read file content.

        Args:
            file_path (str): Path to file.
            encoding (str): File encoding.

        Returns:
            str: File content.
        """
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {file_path}") from e
