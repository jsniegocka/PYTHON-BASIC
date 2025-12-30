import os
from random import randint
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sys
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './output')
RESULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), './output/result.csv')



def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def func1(array: list, output_dir):
    sys.set_int_max_str_digits(0)
    with ProcessPoolExecutor() as executor:
        future = executor.map(fib, array)
        for i, ft in enumerate(future):
            with open(os.path.join(output_dir, str(array[i])), 'w') as f:
                f.write(str(ft))

def func1_slow(array: list, output_dir):
    sys.set_int_max_str_digits(0)
    future = [fib(arr) for arr in array]
    for i, ft in enumerate(future):
        with open(os.path.join(output_dir, str(array[i])), 'w') as f:
            f.write(str(ft))

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

def func2(result_file: str, output_dir: str):
    def process_file(file):
        file_path = os.path.join(output_dir, file)
        with open(file_path, 'r') as f:
            line = f.read()
        ordinal = file.split(".")[0]
        return f"{ordinal},{line}"

    files = os.listdir(output_dir)

    with ThreadPoolExecutor() as executor:
        lines = list(executor.map(process_file, files))
    with open(result_file, 'a') as f:
        for line in lines:
            f.write(line + "\n")

def func2_slow(result_file: str, output_dir):
    with open(result_file, 'a') as f1:
        for file in os.listdir(output_dir):
            line = ""
            with open(os.path.join(output_dir, file), 'r') as f2:
                line = f2.read()
                f1.write(f"{file.split(".")[0]},{line}\n")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    n = 1000
    print(f"Number of elements: {n}")

    print("Starting first function with multiprocessing...")
    time_start = time.time()
    func1(array=[randint(1000, 100000) for _ in range(n)], output_dir=OUTPUT_DIR)
    print(f"First function with multiprocessing execution time: {time.time() - time_start}")

    print("Starting first function without multiprocessing...")
    time_start = time.time()
    func1_slow(array=[randint(1000, 100000) for _ in range(n)], output_dir=OUTPUT_DIR)
    print(f"First function without multiprocessing execution time: {time.time() - time_start}")

    print("Starting second function with multithreading...")
    time_start = time.time()
    func2(result_file=RESULT_FILE, output_dir=OUTPUT_DIR)
    print(f"Second function with multithreading execution time: {time.time() - time_start}")

    print("Starting second function without multithreading...")
    time_start = time.time()
    func2_slow(result_file=RESULT_FILE, output_dir=OUTPUT_DIR)
    print(f"Second function without multithreading execution time: {time.time() - time_start}")


if __name__ == '__main__':
    main()
