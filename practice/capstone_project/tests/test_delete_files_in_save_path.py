from practice.capstone_project.data_generator import delete_files_in_save_path
import os

def test_delete_files_in_save_path_true(tmp_path):
    clear_path = True
    file_name = "file_name.json"
    file_names = []
    for i in range (0, 10):
        file_names.append(f"{file_name.split('.')[0]}_{i}.json")

    for file in file_names:
        with open(os.path.join(tmp_path, file), "w"):
            pass

    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == 10
    delete_files_in_save_path(tmp_path, file_name, clear_path)
    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == 0

def test_delete_files_in_save_path_false(tmp_path):
    clear_path = False
    file_name = "file_name.json"
    file_names = []
    for i in range (0, 10):
        file_names.append(f"{file_name.split('.')[0]}_{i}.json")

    for file in file_names:
        with open(os.path.join(tmp_path, file), "w"):
            pass

    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == 10
    delete_files_in_save_path(tmp_path, file_name, clear_path)
    existing_files = [f for f in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, f))]
    assert len(existing_files) == 10