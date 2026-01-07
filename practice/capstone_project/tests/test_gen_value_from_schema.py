from practice.capstone_project.data_generator import gen_value_from_schema
import pytest
import random
from freezegun import freeze_time
from unittest.mock import patch
from uuid import UUID


@freeze_time("2024-01-01 12:00:00")
@patch("practice.capstone_project.data_generator.uuid.uuid4")
@pytest.mark.parametrize("ds_type, ds_value, expected_gen_value", [
        ("timestamp", "", 1704110400.0),
        ("str", "rand", "f3c28681-349c-4879-a115-65c26bd60eae"),
        ("str", "['a', 'b', 'c']", "c"),
        ("str", "['a' , 'b' , 'c' ]", "c"),
        ("str", "a", "a"),
        ("str", "", ""),
        ("int", "rand", 1824),
        ("int", "rand(0, 5)", 5),
        ("int", "rand(0, 0)", 0),
        ("int", "[1, 2, 3]", 3),
        ("int", "3", 3),
        ("int", "", None)
    ])
def test_gen_value_from_schema(mock_uuid, ds_type, ds_value, expected_gen_value):
    mock_uuid.return_value = UUID("f3c28681-349c-4879-a115-65c26bd60eae")
    random.seed(42)
    gen_value = gen_value_from_schema(ds_type, ds_value)
    print(gen_value)
    assert gen_value == expected_gen_value