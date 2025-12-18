"""
Write tests for module_2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""


import pytest
from module_2_python_part_2.task_read_write_2 import read_write_2
import module_2_python_part_2.task_read_write_2 as mod
from unittest.mock import Mock


@pytest.fixture
def setup_paths(tmp_path):
    output_file1 = tmp_path / "file1.txt"
    output_file2 = tmp_path / "file2.txt"
    return output_file1, output_file2


@pytest.mark.parametrize("words, expected_result1, expected_result2", [
    (["asddfg", "kahfc", "aefj"], "asddfg\nkahfc\naefj", "asddfg,kahfc,aefj"),
    (["", "kahfc", "aefj"], "\nkahfc\naefj", ",kahfc,aefj"),
    (["asddfg"], "asddfg", "asddfg"),
    ([], "", "")]
)


@pytest.mark.read_write_2_basic
def test_read_write_2_basic(setup_paths, words, expected_result1, expected_result2):
    output_file1, output_file2 = setup_paths
    mod.generate_words = Mock(return_value=words)

    read_write_2(mod.generate_words(), file1=str(output_file1), file2=str(output_file2))

    actual_result1 = output_file1.read_text()
    actual_result2 = output_file2.read_text()
    assert actual_result1 == expected_result1
    assert actual_result2 == expected_result2


@pytest.mark.read_write_2_unicode
def test_read_write_2_unicode(setup_paths):
    words = ["ąćęłó", "źż"]
    output_file1, output_file2 = setup_paths
    mod.generate_words = Mock(return_value=words)

    with pytest.raises(UnicodeEncodeError):
        read_write_2(mod.generate_words(), file1=str(output_file1), file2=str(output_file2))

    assert output_file1.read_text(encoding="utf-8") == "ąćęłó\nźż"
    assert output_file2.read_text(encoding="latin-1") == ""
