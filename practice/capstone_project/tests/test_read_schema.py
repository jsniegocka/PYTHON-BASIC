from practice.capstone_project.data_generator import read_data_schema
import pytest
import json

@pytest.fixture
def test_data_schema():
    schema_dict = {
        "date": "timestamp:",
        "name": "str:rand",
        "type": "str:['client', 'partner', 'government']",
        "age": "int:rand(1, 90)"
    }
    schema_json = json.dumps(schema_dict)
    return schema_dict, schema_json


def test_read_data_schema_from_input(test_data_schema):
    schema_dict, schema_json = test_data_schema
    data_schema = read_data_schema(schema_json)
    assert data_schema == schema_dict


def test_read_data_schema_from_file(tmp_path, test_data_schema):
    data_schema_path = tmp_path / 'data_schema.json'
    schema_dict, schema_json = test_data_schema
    json.dump(schema_dict, open(data_schema_path, "w"))
    data_schema = read_data_schema(data_schema_path)
    assert data_schema == schema_dict

