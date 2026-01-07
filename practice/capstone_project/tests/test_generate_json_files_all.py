from practice.capstone_project.data_generator import generate_json_files_all
import os

def test_generate_json_files_all(tmp_path):
    file_name = "file_name.json"
    file_names = []
    for i in range(0, 10):
        file_names.append(f"{file_name.split('.')[0]}_{i}.json")
    data_schema = {"date": "timestamp:", "name": "str:rand", "type": "str:['client', 'partner', 'government']",
                   "age": "int:rand(1, 90)"}
    multiprocessing = 2
    data_lines = 1000
    files_count = 10

    generate_json_files_all(file_names, data_schema, multiprocessing, data_lines, files_count, tmp_path)

    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == len(file_names)
    assert set(existing_files) == set(file_names)

def test_generate_json_files_all_no_files(tmp_path):
    file_name = "file_name.json"
    file_names = []
    for i in range(0, 10):
        file_names.append(f"{file_name.split('.')[0]}_{i}.json")
    data_schema = {"date": "timestamp:", "name": "str:rand", "type": "str:['client', 'partner', 'government']",
                   "age": "int:rand(1, 90)"}
    multiprocessing = 2
    data_lines = 1000
    files_count = 0

    generate_json_files_all(file_names, data_schema, multiprocessing, data_lines, files_count, tmp_path)

    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == 0