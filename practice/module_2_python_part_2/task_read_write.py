"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import os

def read_write(input_dir = "files", output_dir= "result.txt"):
    files = os.listdir(input_dir)
    files.sort(key = lambda name: int(name.split("_")[1].split(".")[0]))
    lines = []
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r") as opened_file:
            for line in opened_file:
                lines.append(line)
    with open(output_dir, "w") as new_file:
        new_file.write(",".join(lines))