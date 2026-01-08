from practice.capstone_project.data_generator import validate_schema_structure, validate_schema_data_types_and_values
import pytest

def test_validate_schema_structure_correct_structure(caplog):
    assert "Incorrect data schema - there is no ':', only data type or value type provided: name:str" not in caplog.text

@pytest.mark.parametrize("data_schema, ds, error", [
        ({"name":"str"}, "name", "Incorrect data schema - there is no ':', only data type or value type provided: name:str"),
        ({"name":"str::"}, "name", "Incorrect data schema - too many ':' : name:str::"),
    ])
def test_validate_schema_structure_incorrect_structure(data_schema, ds, error, caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_structure(data_schema, ds)
    assert exc.value.code == 1
    assert error in caplog.text

@pytest.mark.parametrize("ds_type, ds_value", [
        ("", ""),
        ("", "rand"),
        ("", "['a', 'b', 'c']"),
        ("", "a"),
        ("", "3"),
        ("float", "3.3")
    ])
def test_validate_schema_data_types_and_values_incorrect_ds_type(ds_type, ds_value, caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values(ds_type, ds_value)
    assert exc.value.code == 1
    assert ("Incorrect data type in data schema - value: , data type: <class 'str'>\n" in caplog.text or
            "Incorrect data type in data schema - value: float, data type: <class 'str'>\n" in caplog.text)

def test_validate_schema_data_types_and_values_incorrect_timestamp(caplog):
    validate_schema_data_types_and_values("timestamp", "a")
    assert "Timestamp does not support any values" in caplog.text

def test_validate_schema_data_types_and_values_incorrect_string(caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values("str", "10")
    assert exc.value.code == 1
    assert "Incorrect string format: 10. Integer instead of string" in caplog.text

def test_validate_schema_data_types_and_values_incorrect_integer(caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values("int", "a")
    assert exc.value.code == 1
    assert "Incorrect integer format: a" in caplog.text

@pytest.mark.parametrize("ds_type, ds_value", [
        ("int", "[1, 'a', 3]"),
        ("int", "[1, '2', 3]"),
        ("int", "[]")
    ])
def test_validate_schema_data_types_and_values_incorrect_integer_list(ds_type, ds_value, caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values(ds_type, ds_value)
    assert exc.value.code == 1
    assert ("Incorrect integer list format: [1, 'a', 3]" in caplog.text or
            "Incorrect integer list format: [1, '2', 3]" in caplog.text or
            "Incorrect integer list format: []. Empty list is not allowed" in caplog.text)

def test_validate_schema_data_types_and_values_incorrect_string_list(caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values("str", "[]")
    assert exc.value.code == 1
    assert "Incorrect string list format: []. Empty list is not allowed" in caplog.text

@pytest.mark.parametrize("ds_type, ds_value", [
        ("int", "rand(5, 1)"),
        ("int", "rand(b, 1)")
    ])
def test_validate_schema_data_types_and_values_incorrect_integer_range(ds_type, ds_value, caplog):
    with pytest.raises(SystemExit) as exc:
        validate_schema_data_types_and_values(ds_type, ds_value)
    assert exc.value.code == 1
    assert ("Incorrect range format for rand: rand(5, 1). First number can't be greater than the second number"
            in caplog.text or
            "Incorrect range format for rand: rand(b, 1)" in caplog.text)