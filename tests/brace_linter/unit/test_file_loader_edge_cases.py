import pytest
import tempfile
import os
from pycleancode.brace_linter.filesystem.file_loader import FileLoader


def test_file_loader_non_py_file_ignored():
    with tempfile.TemporaryDirectory() as tmp_dir:
        txt_path = os.path.join(tmp_dir, "file.txt")
        with open(txt_path, "w") as f:
            f.write("Should be ignored")

        loader = FileLoader()
        files = loader.load_files(tmp_dir)
        assert files == {}


def test_file_loader_file_not_found():
    loader = FileLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_files("non_existing_file.py")
