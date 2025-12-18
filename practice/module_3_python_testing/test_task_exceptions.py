"""
Write tests for division() function in module_2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

import pytest
from module_2_python_part_2.task_exceptions import division, DivisionByOneException


@pytest.mark.parametrize("numbers, expected_output", [
    ((6,3),2),
    ((7,2),3),
    ((6,-2),-3),
    ((-6,-2),3)]
)

def test_division_ok(capfd, numbers, expected_output):
    assert division(numbers[0], numbers[1]) == expected_output


def test_division_by_zero(capfd):
    assert division(1, 0) is None
    out, err = capfd.readouterr()
    assert "Division by 0" in out


def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException):
        division(6, 1)