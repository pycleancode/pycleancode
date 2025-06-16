"""
Module: file_loader

Provides functionality to load Python source files from a file path or directory.
"""

import os
from typing import Dict


class FileLoader:
    """
    FileLoader loads source files from a file or recursively from a directory.
    """

    def __init__(self, extension: str = ".py") -> None:
        """
        Initialize FileLoader with a file extension filter.
        """
        self.extension = extension

    def load_files(self, path: str) -> Dict[str, str]:
        """
        Load files from the provided path.

        Args:
            path (str): A file or directory path.

        Returns:
            Dict[str, str]: A dictionary of file paths and their contents.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")

        if os.path.isfile(path):
            return self._load_single_file(path)

        return self._load_directory(path)

    def _load_single_file(self, path: str) -> Dict[str, str]:
        """
        Load a single file if it matches the extension.
        """
        if not path.endswith(self.extension):
            return {}
        return {path: self._read_file(path)}

    def _load_directory(self, directory: str) -> Dict[str, str]:
        """
        Load all files in a directory that match the extension.
        """
        files: Dict[str, str] = {}

        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if not filename.endswith(self.extension):
                    continue

                full_path = os.path.join(root, filename)
                files[full_path] = self._read_file(full_path)

        return files

    def _read_file(self, filepath: str) -> str:
        """
        Read file content.
        """
        try:
            with open(filepath, encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {filepath}") from e
