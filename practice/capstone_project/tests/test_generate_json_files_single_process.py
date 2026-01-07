from practice.capstone_project.data_generator import generate_json_files_single_process
import os

def test_generate_json_files_single_process(tmp_path):
    file_name = "file_name.json"
    file_names = []
    for i in range(0, 10):
        file_names.append(f"{file_name.split('.')[0]}_{i}.json")
    data_schema = {"date": "timestamp:", "name": "str:rand", "type": "str:['client', 'partner', 'government']",
                   "age": "int:rand(1, 90)"}
    data_lines = 1000
    files_count = 10
    generate_json_files_single_process(file_names, data_schema, data_lines, files_count, tmp_path)
    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == len(file_names)
    assert set(existing_files) == set(file_names)
    for file in existing_files:
        with open(tmp_path / file, "r") as f:
            lines = f.readlines()
            assert len(lines) == data_lines