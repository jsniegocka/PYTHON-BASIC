"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
from module_2_python_part_2.task_input_output import read_numbers

def test_read_numbers_without_text_input():
    with patch("module_2_python_part_2.task_input_output.get_user_input", side_effect=[3, 6, 3]):
        output = read_numbers(3)
    assert output == "Avg: 4.0"


def test_read_numbers_with_text_input():
    with patch("module_2_python_part_2.task_input_output.get_user_input", side_effect=["hgdja", "hdklw", "oehak", "alkdrn"]):
        output = read_numbers(4)
    assert output == "No numbers entered"


def test_read_numbers_with_mixed_input():
    with patch("module_2_python_part_2.task_input_output.get_user_input", side_effect=["4", "hdklw", "162", "alkdrn"]):
        output = read_numbers(4)
    assert output == "Avg: 83.0"

