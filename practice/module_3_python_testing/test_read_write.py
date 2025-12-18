"""
Write tests for module_2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import pytest
from module_2_python_part_2.task_read_write import read_write

@pytest.mark.parametrize("file_contents, expected_result", [
    (["23", "78", "3"], "23,78,3"),
    (["", "78", "3"], "78,3"),
    (["a", "b", "c"], "a,b,c"),
    (["23"], "23"),
    ([], "")]
)
@pytest.mark.read_write_basic
def test_read_write_basic(tmp_path, file_contents, expected_result):
    input_dir = tmp_path / "files"
    input_dir.mkdir()
    output_dir = tmp_path / "result.txt"

    for i, content in enumerate(file_contents):
        file_path = input_dir / f"_{i}.txt"
        file_path.write_text(content)
    read_write(input_dir=str(input_dir), output_dir=str(output_dir))

    actual_result = output_dir.read_text()
    assert actual_result == expected_result