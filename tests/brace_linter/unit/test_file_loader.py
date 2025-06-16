import os
import tempfile
from pathlib import Path

import pytest

from pycleancode.brace_linter.filesystem.file_loader import FileLoader


@pytest.fixture
def file_loader() -> FileLoader:
    return FileLoader()


def test_load_single_file(file_loader: FileLoader) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write("print('Hello')")
        temp_file_path = temp_file.name

    try:
        files = file_loader.load_files(temp_file_path)
        assert temp_file_path in files
        assert files[temp_file_path] == "print('Hello')"
    finally:
        os.remove(temp_file_path)


def test_load_directory(file_loader: FileLoader) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = Path(temp_dir) / "file1.py"
        file2 = Path(temp_dir) / "file2.py"
        file3 = Path(temp_dir) / "not_python.txt"

        file1.write_text("print('file1')")
        file2.write_text("print('file2')")
        file3.write_text("some text")

        files = file_loader.load_files(temp_dir)

        assert len(files) == 2
        assert str(file1) in files
        assert str(file2) in files
        assert str(file3) not in files
        assert files[str(file1)] == "print('file1')"


def test_load_empty_directory(file_loader: FileLoader) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        files = file_loader.load_files(temp_dir)
        assert files == {}
