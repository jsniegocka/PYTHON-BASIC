# -*- coding: utf-8 -*-

"""

Data Generator
Capstone Project
Author: Julia Śniegocka

Universal Console Utility (CU) for generating test data based on the provided data schema.
Data schema format: json, special notation “type:what_to_generate”
Output data format: json

Parameters:

--path_to_save_files (default: ".")
    Path in which generated data will be saved ("." means current path).

--files_count (default: 0)
    Number of json files to generate (0 means print all output to console).

--file_name (default: "file_name.json")
    Base json file_name. If there is no prefix, the final file name will be file_name.json.
    With prefix, full file name will be file_name_file_prefix.json.

--file_prefix (default: "count", choices: count, random, uuid)
    Prefix for file name to use if more than 1 file is generated.

--data_schema (default: '{"date": "timestamp:", "name": "str:rand", "type": "str:[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}')
    String with JSON schema. Can be loaded from a file or entered in the command line. Needs to follow 'Data Schema Parse' protocols:
    Data Schema Parse:
    All values support special notation 'type:what_to_generate':
        - ':' in value indicates that the left part of the value is a type.
        - Type could be: timestamp, str, and int.
    For the right part of values with ':' notation, there are 5 possible options:
        - rand - random generation:
            - If on the left there is 'str' type, uuid4 is used for generation.
            - If on the left there is 'int' type, random.randint(0, 10000) is used for generation.
        - List with values '[]', for example, 'str:[\'client\', \'partner\', \'government\']' or 'int:[0, 9, 10, 4]', takes a random value from the list.
        - rand(from, to) - random generation for int values in the prescribed range. Possible to use only with 'int' type.
        - Stand-alone value: if in the schema after ':' a value is written which has a type corresponding with the left part.
            For example, for 'name': 'str:cat', the script generates 'name':'cat' for each line.
        - Empty value: for any type:
            - For 'int', uses None.
            - For 'str', uses an empty string ''.
            - For 'timestamp' type, all values after ':' should be ignored.

--data_lines (default: 1000)
    Count of lines for each file.

--clear_path (default: False)
    Flag indicating if all files in path_to_save_files that match file_name will be deleted before generating new files.
--multiprocessing (default: 1)
    Number of processes used to create files. Divides the files_count value equally and starts N processes to create
    files in parallel.


"""

import argparse
import configparser
import os
import logging
import json
import time
from concurrent.futures import ProcessPoolExecutor

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

log = logging.getLogger()

def read_config_file() -> argparse.Namespace:
    """Reading default.ini configuration file"""
    log.info("Reading configuration file...")
    config = configparser.ConfigParser()
    files_read = config.read(os.path.join(SCRIPT_PATH, "default.ini"))
    if not files_read:
        log.error(f"Configuration file default.ini parsing error")
        exit(1)
    log.info("Configuration file has been read")
    return config

def create_parser() -> argparse.ArgumentParser:
    """Creating parser"""
    log.info("Creating parser...")
    parser = argparse.ArgumentParser(
        prog="data_generator",
        description="Universal Console Utility (CU) for generating test data based on the provided data schema.")
    log.info("Parser has been created")
    return parser

def add_parser_arguments(parser: argparse.ArgumentParser, config) -> None:
    """Adding parser arguments"""
    log.info("Adding parser arguments...")
    parser.add_argument("--path_to_save_files",
                        nargs="?",
                        default=config["DEFAULT"]["path_to_save_files"],
                        type=str,
                        help="Path in which generated data will be saved (`.` means current path).")

    parser.add_argument("--files_count",
                        nargs="?",
                        default=config["DEFAULT"]["files_count"],
                        type=int,
                        help="Number of json files to generate (0 means print all output to console).")

    parser.add_argument("--file_name",
                        nargs="?",
                        default=config["DEFAULT"]["file_name"],
                        type=str,
                        help="Base json file_name. If there is no prefix, the final file name will be file_name.json. \
                                With prefix full file name will be file_name_file_prefix.json.")

    parser.add_argument("--file_prefix",
                        nargs="?",
                        default=config["DEFAULT"]["file_prefix"],
                        type=str,
                        choices=["count", "random", "uuid"],
                        help="Prefix for file name to use if more than 1 file is generated")

    parser.add_argument("--data_schema",
                        nargs="?",
                        default=config["DEFAULT"]["data_schema"],
                        type=str,
                        help=
                        "String with json schema. It could be loaded in two ways:\n"
                        "1) With the path to a JSON file with schema\n"
                        "2) With schema entered in the command line.\n"
                        "Data Schema must follow 'Data Schema Parse' protocols: \n"
                        "All values support special notation 'type:what_to_generate': \n"
                        "- ':' in value indicates that the left part of the value is a type.\n"
                        "- The type could be: timestamp, str, and int.\n"
                        "For the right part of values with ':' notation, possible options are:\n"
                        "    - 'rand' (random generation):\n"
                        "        - If on the left, there is 'str' type, uuid4 is used for generation.\n"
                        "        - If on the left, there is 'int' type, random.randint(0, 10000) is used for generation.\n"
                        "    - List with values '[]', for example, 'str:[\'client\', \'partner\', \'government\']' or "
                        "'int:[0, 9, 10, 4]' — takes a random value from the list.\n"
                        "    - 'rand(from, to)' — random generation for int values in the prescribed range. Possible only with 'int' type.\n"
                        "    - Stand-alone value: If in the schema, after ':', a value is written which has a type corresponding "
                        "to the left part. For example, for 'name': 'str:cat', the script generates 'name':'cat' for each line.\n"
                        "    - Empty value: For any type, the following applies:\n"
                        "        - For 'int', uses None.\n"
                        "        - For 'str', uses an empty string ('').\n"
                        "        - For 'timestamp' type, all values after ':' should be ignored.\n")

    parser.add_argument("--data_lines",
                        nargs="?",
                        default=config["DEFAULT"]["data_lines"],
                        type=int,
                        help="Count of lines for each file (default: 1000).")

    parser.add_argument("--clear_path",
                        action="store_true",
                        default=config["DEFAULT"]["clear_path"],
                        help="Flag indicating if all files in path_to_save_files that match file_name will be deleted \
                                before the script starts creating new data files.")

    parser.add_argument("--multiprocessing",
                        nargs="?",
                        default=config["DEFAULT"]["multiprocessing"],
                        type=int,
                        help="The number of processes used to create files. Divides the “files_count” value equally \
                                and starts N processes to create an equal number of files in parallel (optional argument, \
                                default value: 1.")

    log.info("Parser arguments have been added")

def setup_parser() -> argparse.ArgumentParser:
    """Setting up console utility"""
    log.info("Setting up console utility...")

    # Reading configuration file
    config = read_config_file()

    # Creating parser
    parser = create_parser()

    # Adding parser arguments
    add_parser_arguments(parser, config)

    log.info("Console utility has been set up")
    return parser

def save_console_utility_parameters(parser:argparse.ArgumentParser) -> dict:
    """Saving console utility arguments"""
    log.info("Saving console utility parameters...")
    args_dict = vars(parser.parse_args())
    log.info(f"Console Utility parameters: {args_dict}")  # showing console utility arguments
    log.info("Console utility parameters have been saved")
    return args_dict

def read_data_schema(data_schema:str) -> dict:
    """Reading data schema from json file or input"""
    log.info("Reading data schema...")
    if os.path.exists(data_schema) and os.path.isfile(data_schema):
        log.info(f"Loading data schema from file: {data_schema}")
        with open(data_schema, "r") as f:
            log.info("Data schema has been read")
            return json.load(f)
    else:
        return json.loads(data_schema)

def gen_file_names(files_count:int, file_name:str, file_prefix:str) -> list:
    """Generating file names"""
    log.info("Generating file names...")

    # If there is only one file, return name without prefix
    file_names = []
    if files_count == 1:
        file_names = [file_name]
        log.info("File names generated")
        return file_names

    # If there are multiple files, return names with prefix
    log.info(f"Generating file names using prefix: {file_prefix} ...")
    for c in range(files_count):
        file_names.append(f"{file_name}_{c+1}.json")
    log.info("File names generated")
    return file_names

def write_single_json_file(data_schema:dict, filename:str, path_to_save_files:str) -> None:
    """Writing single json file"""
    log.info(f"Writing json file: {filename} ...")
    with open(os.path.join(path_to_save_files, filename), "w") as f:
        json.dump(data_schema, f, indent=4)
    log.info(f"File {filename} has been written")

def setup_output_for_directory(fnl:list, data_schema:dict, path_to_save_files:str) -> None:
    """Setting up output for directory"""
    # Generating multiple files
    for filename in fnl:
        # Generating singular file
        log.info(f"Generating json file: {filename} ...")

        # Writing singular file
        write_single_json_file(data_schema, filename, path_to_save_files)

        log.info(f"File {filename} has been generated")

def generate_json_files_multiple_processes(split_file_names_list:list, data_schema:dict, path_to_save_files:str) -> None:
    """Coordinate generating multiple .json files in multiple processes (using multiprocessing)"""
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                setup_output_for_directory,
                fnl,
                data_schema,
                path_to_save_files
            )
            for fnl in split_file_names_list
        ]

        for future in futures:
            future.result()

def split_list_evenly(lst:list, n:int) -> list:
    """Splitting list evenly"""
    return [lst[i::n] for i in range(n)]

def generate_json_files_all(file_names:list, data_schema:dict, multiprocessing:int,  path_to_save_files:str) -> None:
    """Coordinate generating all json files"""
    log.info("Starting multiprocessing...")

    # Splitting files into different processes
    log.info("Splitting files for multiprocessing...")
    split_file_names_list = split_list_evenly(file_names, multiprocessing)
    log.info("Files for multiprocessing have been split")

    # Generating multiple .json files in multiple processes
    time_start = time.time() # saving start time to measure execution time
    log.info(f"Starting generation of json files with multiprocessing. Start time: {time.strftime("%H:%M:%S", time.localtime(time_start))}")
    generate_json_files_multiple_processes(split_file_names_list, data_schema, path_to_save_files)
    log.info(
        f"Generation of json files has ended. End time: {time.strftime("%H:%M:%S", time.localtime(time.time()))}. Multiprocessing execution time: {round(time.time() - time_start, 4)} seconds")


def data_generator():
    """Coordinate data generation"""
    # Setting up parser and saving console utility parameters
    parser = setup_parser()
    args_dict = save_console_utility_parameters(parser)

    # Reading data schema
    data_schema = read_data_schema(args_dict["data_schema"])

    # Generating file names
    file_names = gen_file_names(args_dict["files_count"], args_dict["file_name"], args_dict["file_prefix"])

    # Generate files
    generate_json_files_all(file_names,
                            data_schema,
                            args_dict["multiprocessing"],
                            args_dict["path_to_save_files"])

if __name__ == '__main__':
    data_generator()