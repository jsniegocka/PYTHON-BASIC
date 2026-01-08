from practice.capstone_project.data_generator import gen_file_names
import os

def test_gen_file_names_count_prefix(tmp_path):
    names = gen_file_names(3, "file_name", "count", tmp_path)
    assert names == ["file_name_1.json", "file_name_2.json", "file_name_3.json"]

def test_gen_file_names_count_prefix_multiple_generations(tmp_path):
    names = gen_file_names(3, "file_name", "count", tmp_path)
    for name in names:
        open(os.path.join(tmp_path, name), "w").close()
    assert names == ["file_name_1.json", "file_name_2.json", "file_name_3.json"]
    names = gen_file_names(3, "file_name", "count", tmp_path)
    assert names == ["file_name_4.json", "file_name_5.json", "file_name_6.json"]

def test_gen_file_names_random_prefix(tmp_path):
    names = gen_file_names(3, "file_name", "random", tmp_path)
    assert all(name.startswith("file_name_") and name.endswith(".json") for name in names)
    assert all(name.split("_")[2].rstrip(".json").isdigit() for name in names) # all names contain a number

def test_gen_file_names_uuid_prefix(tmp_path):
    names = gen_file_names(3, "file_name", "uuid", tmp_path)
    for name in names:
        uuid_part = name.split("_")[2].split(".json")[0]
        assert len(uuid_part) == 36 # is valid uuid
