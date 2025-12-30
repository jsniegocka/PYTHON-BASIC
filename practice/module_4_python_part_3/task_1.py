from datetime import datetime
import re

class IncorrectFormat(Exception):
    pass

def calculate_days(from_date: str) -> int:
    today = datetime.today().date()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", from_date):
        raise IncorrectFormat("The date entered is not in the correct format")
    chosen_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    number_of_days = (today - chosen_date).days
    return number_of_days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

import pytest
from freezegun import freeze_time

@freeze_time("2021-10-06")
def test_calculate_days_future_date():
    assert calculate_days("2021-10-07") == -1

@freeze_time("2021-10-06")
def test_calculate_days_past_date():
    assert calculate_days('2021-10-05') == 1

@freeze_time("2021-10-06")
def test_calculate_days_incorrect_date():
    with pytest.raises(IncorrectFormat):
        calculate_days("10-07-2021")