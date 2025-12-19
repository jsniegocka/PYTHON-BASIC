"""
Write function which receives filename and reads file line by line and returns min and mix integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename')
    (-2, 34)

Hint:
To read file line-by-line you can use this:
with open(filename) as opened_file:
    for line in opened_file:
        ...
"""
from typing import Tuple
import os


def get_min_max(filename: str) -> Tuple[int, int]:
    file_path = os.path.join(os.path.dirname(__file__), filename)
    lines = []
    with open(file_path, "r") as opened_file:
        for line in opened_file:
            lines.append(int(line))
    return (min(lines), max(lines))

if __name__ == '__main__':
    print(get_min_max('task6.txt'))