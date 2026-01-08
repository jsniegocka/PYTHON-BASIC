from practice.capstone_project.data_generator import gen_line_from_schema
import pytest
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
@pytest.mark.parametrize("data_schema, checks", [
    (
        {
            "date": "timestamp:",
            "name": "str:rand",
            "type": "str:['client', 'partner', 'government']",
            "age": "int:rand(1, 90)"},
        [
            lambda r: r["date"] == 1704110400.0,
            lambda r: isinstance(r["name"], str),
            lambda r: r["type"] in ["client","partner","government"],
            lambda r: isinstance(r["age"], int) and 1 <= r["age"] <= 90
        ]
    ),
    (
        {
            "date": "timestamp:",
            "user_id": "int:rand(1, 1000)",
            "role": "str:['admin','user','guest']",
        },
        [
            lambda r: r["date"] == 1704110400.0,
            lambda r: isinstance(r["user_id"], int) and 1 <= r["user_id"] <= 1000,
            lambda r: r["role"] in ["admin","user","guest"],
        ]
    ),
    (
        {
            "created_at": "timestamp:",
            "segment_number": "int:[1, 2, 3]",
            "segment": "str:['A','B','C']",
        },
        [
            lambda r: r["created_at"] == 1704110400.0,
            lambda r: isinstance(r["segment_number"], int) and r["segment_number"] in [1, 2, 3],
            lambda r: r["segment"] in ["A","B","C"],
        ]
    )
])
def test_gen_line_from_schema(data_schema, checks):
    gen_line = gen_line_from_schema(data_schema)
    assert set(gen_line.keys()) == set(data_schema.keys())
    assert len(gen_line) == len(data_schema)
    for check in checks:
        assert check(gen_line)
