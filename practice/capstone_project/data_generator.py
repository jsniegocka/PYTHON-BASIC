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
import sys
import logging
import json
import uuid
import random
from datetime import datetime
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
        description="Universal Console Utility (CU) for generating test data based on the provided data schema.",
        formatter_class=argparse.RawTextHelpFormatter)
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
                        help="Base json file_name. If there is no prefix, the final file name will be file_name.json. \n"
                             "With prefix full file name will be file_name_file_prefix.json.")

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
                        "    - List with values '[]', for example, 'str:[\'client\', \'partner\', \'government\']' or \n"
                        "'int:[0, 9, 10, 4]' — takes a random value from the list.\n"
                        "    - 'rand(from, to)' — random generation for int values in the prescribed range. Possible only with 'int' type.\n"
                        "    - Stand-alone value: If in the schema, after ':', a value is written which has a type corresponding \n"
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
                        help="Flag indicating if all files in path_to_save_files that match file_name will be deleted \n"
                             "before the script starts creating new data files.")

    parser.add_argument("--multiprocessing",
                        nargs="?",
                        default=config["DEFAULT"]["multiprocessing"],
                        type=int,
                        help="The number of processes used to create files. Divides the “files_count” value equally \n"
                             "and starts N processes to create an equal number of files in parallel (optional argument, \n"
                             "default value: 1.")

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

def check_args_dict(args_dict:dict) -> None:
    log.info("Checking if console utility arguments are valid...")
    if args_dict["files_count"] < 0:
        log.error(f"Number of files can't be negative: {args_dict['files_count']}")
        sys.exit(1)
    if args_dict["data_lines"] < 0:
        log.error(f"Number of lines in file can't be negative: {args_dict['data_lines']}")
        sys.exit(1)
    if args_dict["multiprocessing"] < 0:
        log.error(f"Number of processes can't be negative: {args_dict['multiprocessing']}")
        sys.exit(1)
    if args_dict["file_name"].count(".") > 1:
        log.error(f"File name contains more than one '.': {args_dict['file_name']}")
        sys.exit(1)
    if "." in args_dict["file_name"] and args_dict["file_name"].count(".") == 1:
        if args_dict["file_name"].split(".")[1] != "json":
            log.error(f"Incorrect file extension: {args_dict['file_name']}")
            sys.exit(1)
        else:
            args_dict["file_name"] = args_dict["file_name"].split(".")[0]
    log.info("Console utility arguments are valid")

def save_console_utility_parameters(parser:argparse.ArgumentParser) -> dict:
    """Saving console utility arguments"""
    log.info("Saving console utility parameters...")
    args_dict = vars(parser.parse_args())
    log.info(f"Console Utility parameters: {args_dict}")  # showing console utility arguments
    log.info("Console utility parameters have been saved")
    return args_dict

def set_path_to_save_files(path_to_save_files:str) -> str:
    """Setting path to save output files"""
    log.info("Setting path for saving output files...")

    try:
        if path_to_save_files == ".":
            path_to_save_files = os.getcwd()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            path_to_save_files = os.path.join(path_to_save_files, "generated_files", timestamp)
            log.info("Path to save files set in current directory")
        else:
            path_to_save_files = os.path.abspath(path_to_save_files)
            log.info("Path to save files set in custom directory")

        if os.path.exists(path_to_save_files) and not os.path.isdir(path_to_save_files):
            log.error(f"Provided path exists but is not a directory: {path_to_save_files}")
            sys.exit(1)

        log.info(f"Path to save files set in: {path_to_save_files}")
        os.makedirs(path_to_save_files, exist_ok=True)
        return path_to_save_files

    except Exception as e:
        log.error(f"Failed to create directory '{path_to_save_files}': {e}")
        sys.exit(1)

def delete_files_in_save_path(path_to_save_files:str, file_name:str, clear_path:bool) -> None:
    """Deleting all files in save path that match file_name"""
    if clear_path:
        log.info("Deleting all files in path_to_save_files that match file_name...")
        for filename in os.listdir(path_to_save_files):
            file_path = os.path.join(path_to_save_files, filename)
            if os.path.isfile(file_path) and filename.endswith(".json") and filename.startswith(file_name.split('.')[0]):
                os.remove(file_path)
        log.info("All files in path_to_save_files that match file_name have been deleted")

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

def validate_schema_structure(data_schema: dict, ds:str) -> None:
    """Validating structure of data schema"""
    if ":" not in data_schema[ds] and "timestamp" not in data_schema[ds]:
        log.error(f"Incorrect data schema - there is no ':', only data type or value type provided: {ds}:{data_schema[ds]}")
        sys.exit(1)
    if data_schema[ds].count(":") != 1 and "timestamp" not in data_schema[ds]:
        log.error(f"Incorrect data schema - too many ':' : {ds}:{data_schema[ds]}")
        sys.exit(1)
    if data_schema[ds].count(":")  > 1:
        log.error(f"Incorrect data schema - too many ':' : {ds}:{data_schema[ds]}")
        sys.exit(1)

def validate_value_timestamp(ds_value:str) -> None:
    """Validating timestamp in data schema"""
    if ds_value != "":
        log.warning("Timestamp does not support any values")

def validate_value_str(ds_value:str) -> None:
    """Validating string in data schema"""
    if ds_value == "": pass
    elif ds_value == "rand": pass
    elif ds_value == "[]":
        log.error(f"Incorrect string list format: {ds_value}. Empty list is not allowed")
        sys.exit(1)
    elif ds_value[0] == "[" and ds_value[-1] == "]": pass
    elif isinstance(ds_value, str):
        try:
            int(ds_value)
            log.error(f"Incorrect string format: {ds_value}. Integer instead of string")
            sys.exit(1)
        except ValueError:
            pass
    elif not isinstance(ds_value, str):
        log.error(f"Incorrect string format: {ds_value}")
        sys.exit(1)

def validate_value_int(ds_value:str) -> None:
    """Validating integer in data schema"""
    if ds_value == "":
        pass
    elif ds_value == "[]":
        log.error(f"Incorrect integer list format: {ds_value}. Empty list is not allowed")
        sys.exit(1)
    elif "rand" in ds_value:
        try:
            start, end = map(int, ds_value.removeprefix("rand(").removesuffix(")").split(","))
            if start > end:
                log.error(
                    f"Incorrect range format for rand: {ds_value}. First number can't be greater than the second number")
                sys.exit(1)
            random.randint(start, end)
        except ValueError:
            log.error(f"Incorrect range format for rand: {ds_value}")
            sys.exit(1)
    elif ds_value[0] == "[" and ds_value[-1] == "]":
        rand = [x.strip() for x in ds_value[1:-1].split(",")]
        if not all(x.isdigit() for x in rand):
            log.error(f"Incorrect integer list format: {ds_value}")
            sys.exit(1)
    else:
        try:
            int(ds_value)
        except ValueError:
            log.error(f"Incorrect integer format: {ds_value}")
            sys.exit(1)

def validate_schema_data_types_and_values(ds_type:str, ds_value:str) -> None:
    """Coordinate validating data schema data types and data values"""
    match ds_type:
        case "timestamp":
            validate_value_timestamp(ds_value)
        case "str":
            validate_value_str(ds_value)
        case "int":
            validate_value_int(ds_value)
        case _:
            log.error(f"Incorrect data type in data schema - value: {ds_type}, data type: {type(ds_type)}")
            sys.exit(1)

def validate_schema(data_schema:dict) -> None:
    """Validating data schema"""
    log.info("Validating data schema...")
    for i, ds in enumerate(data_schema.keys()):
        validate_schema_structure(data_schema, ds)
        ds_type, ds_value = "", ""
        if ":" in data_schema[ds]:
            ds_type, ds_value = data_schema[ds].split(":")
        elif "timestamp" in data_schema[ds]:
            ds_type = data_schema[ds]
        validate_schema_data_types_and_values(ds_type, ds_value)
        log.info("Data schema validated")

        validate_schema_data_types_and_values(ds_type, ds_value)
    log.info("Data schema validated")

def get_unique_filename(base_name: str, path_to_save_files: str) -> str:
    """Return unique file name"""
    filename = f"{base_name}.json"
    if not os.path.exists(os.path.join(path_to_save_files, filename)):
        return filename

    counter = 1
    while os.path.exists(os.path.join(path_to_save_files, filename)):
        filename = f"{base_name}_{counter}.json"
        counter += 1

    return filename

def gen_file_names(files_count:int, file_name:str, file_prefix:str, path_to_save_files:str) -> list:
    """Generating file names"""
    log.info("Generating file names...")

    # If there is only one file, return name without prefix
    file_names = []
    if files_count == 1:
        file_names = [f"{file_name}.json"]
        log.info("File names generated")
        return file_names

    # If there are multiple files, return names with prefix
    log.info(f"Generating file names using prefix: {file_prefix} ...")
    match file_prefix:
        case "count":
            existing = [
                int(f.split("_")[-1].split(".")[0])
                for f in os.listdir(path_to_save_files)
                if f.startswith(file_name + "_") and f.endswith(".json")
            ]
            start_num = max(existing, default=0) + 1

            for c in range(start_num, start_num + files_count):
                file_names.append(f"{file_name}_{c}.json")
        case "random":
            for c in range(files_count):
                name = get_unique_filename(f"{file_name}_{random.randint(0, max(10000, files_count))}",
                                         path_to_save_files)
                file_names.append(name)
        case "uuid":
            for c in range(files_count):
                name = get_unique_filename(f"{file_name}_{uuid.uuid4()}", path_to_save_files)
                file_names.append(name)
    log.info("File names generated")
    return file_names

def split_list_evenly(lst:list, n:int) -> list:
    """Splitting list evenly"""
    return [lst[i::n] for i in range(n)]

def gen_value_str(ds_value:str) -> str:
    """Generating a string value from schema"""
    if ds_value == "":
        return ""
    elif ds_value == "rand":
        return str(uuid.uuid4())
    elif ds_value[0] == "[" and ds_value[-1] == "]":
        return random.choice([x.strip().strip("'") for x in ds_value[1:-1].split(",")])
    else:
        return ds_value

def gen_value_int(ds_value:str) -> int|None:
    """Generating a integer value from schema"""
    if ds_value == "":
        return None
    elif ds_value == "rand":
        return random.randint(0, 10000)
    elif "rand" in ds_value:
        start, end = map(int, ds_value.removeprefix("rand(").removesuffix(")").split(","))
        rand_num = random.randint(start, end)
        return rand_num
    elif ds_value[0] == "[" and ds_value[-1] == "]":
        rand = [x.strip() for x in ds_value[1:-1].split(",")]
        rand_int = int(random.choice(rand))
        return rand_int
    else:
        ds_int = int(ds_value)
        return ds_int

def gen_value_from_schema(ds_type:str, ds_value:str) -> str|int|float|None:
    """Generating a singular value from schema, based on parameters from special notation"""
    match ds_type:
        case "timestamp":
            return time.time()
        case "str":
            return gen_value_str(ds_value)
        case "int":
            return gen_value_int(ds_value)
        case _:
            return None

def gen_line_from_schema(data_schema:dict) -> dict:
    """Set up generating a singular line from shema"""
    gen_line_dict = {}
    for i, ds in enumerate(data_schema.keys()):
        if ":" in data_schema[ds]:
            ds_type, ds_value = data_schema[ds].split(":")
        else:
            ds_type = data_schema[ds]
            ds_value = ""
        gen_value = gen_value_from_schema(ds_type, ds_value)
        gen_line_dict[ds] = gen_value
    return gen_line_dict

def join_gen_lines(data_schema:dict, data_lines:int) -> list:
    """Joining generated lines into a singular .json file"""
    lines = []
    for l in range(data_lines):
        # Generating a singular line from shema
        gen_line = gen_line_from_schema(data_schema)
        lines.append(gen_line)
    return lines

def write_single_json_file(lines:list, filename:str, path_to_save_files:str) -> None:
    """Writing single json file"""
    log.info(f"Writing json file: {filename} ...")
    with open(os.path.join(path_to_save_files, filename), "w") as f:
        f.write("\n".join(json.dumps(line) for line in lines))
    log.info(f"File {filename} has been written")

def gen_output_for_console(data_schema:dict, data_lines:int) -> list:
    """Generating lines for console output"""
    log.info(f"Generating lines for the console...")
    lines = join_gen_lines(data_schema, data_lines)
    log.info(f"Lines for console have been generated")
    return lines

def print_output_to_console(lines:list) -> None:
    """Printing output to console"""
    for line in lines:
        print(line, "\n")

def setup_output_for_console(data_schema:dict, data_lines:int) -> None:
    """Setting up output for console"""

    # Generate lines for the console
    lines = gen_output_for_console(data_schema, data_lines)

    # Print lines to console
    print_output_to_console(lines)

def gen_output_for_directory(filename:str, data_schema:dict, data_lines:int) -> list:
    """Generating lines for json file"""
    log.info(f"Generating lines for json file: {filename} ...")
    lines = join_gen_lines(data_schema, data_lines)
    log.info(f"Lines for json file {filename} have been generated")
    return lines

def setup_output_for_directory(fnl:list, data_schema:dict, data_lines:int, path_to_save_files:str) -> None:
    """Setting up output for directory"""
    # Generating multiple files
    for filename in fnl:
        # Generating singular file
        log.info(f"Generating json file: {filename} ...")

        # Generating output for directory
        lines = gen_output_for_directory(filename, data_schema, data_lines)

        # Writing singular file
        write_single_json_file(lines, filename, path_to_save_files)

        log.info(f"File {filename} has been generated")

def generate_json_files_single_process(fnl:list, data_schema:dict, data_lines:int, files_count:int, path_to_save_files:str) -> None:
    """Coordinate generating multiple .json files in a singular process (deciding type of output)"""

    # Deciding type of output
    if files_count == 0:  # checking if number of files is 0
        setup_output_for_console(data_schema, data_lines)
    else:
        setup_output_for_directory(fnl, data_schema, data_lines, path_to_save_files)

def generate_json_files_multiple_processes(split_file_names_list:list, data_schema:dict, data_lines:int, files_count:int, path_to_save_files:str) -> None:
    """Coordinate generating multiple .json files in multiple processes (using multiprocessing)"""
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                generate_json_files_single_process,
                fnl,
                data_schema,
                data_lines,
                files_count,
                path_to_save_files
            )
            for fnl in split_file_names_list
        ]

        for future in futures:
            future.result()

def check_number_of_processes(multiprocessing:int) -> int:
    """Checking what number of processes has been set and if it is appropriate"""
    log.info("Checking number of processes...")
    if multiprocessing > os.cpu_count():
        multiprocessing = os.cpu_count()
        log.warning(f"Number of processes too high - changed the number to cpu count: {os.cpu_count()}")
    log.info(f"Number of processes is correct and has been set: {multiprocessing}")
    return multiprocessing

def check_number_of_files(files_count:int) -> None:
    """Checking what number of files has been set and if it is appropriate"""
    log.info("Checking number of files...")
    if files_count == 0:
        log.warning("Number of files is 0. Printing all the output to the console")
    log.info("Number of files has been checked")

def generate_json_files_all(file_names:list, data_schema:dict, multiprocessing:int, data_lines:int, files_count:int,  path_to_save_files:str) -> None:
    """Coordinate generating all json files"""
    log.info("Starting multiprocessing...")

    # Splitting files into different processes
    log.info("Splitting files for multiprocessing...")
    split_file_names_list = split_list_evenly(file_names, multiprocessing)
    log.info("Files for multiprocessing have been split")

    # Generating multiple .json files in multiple processes
    time_start = time.time() # saving start time to measure execution time
    log.info(f"Starting generation of json files with multiprocessing. "
             f"Start time: {time.strftime('%H:%M:%S', time.localtime(time_start))}")
    generate_json_files_multiple_processes(split_file_names_list, data_schema, data_lines, files_count,
                                           path_to_save_files)
    log.info(
        f"Generation of json files has ended. "
        f"End time: {time.strftime('%H:%M:%S', time.localtime(time.time()))}. "
        f"Multiprocessing execution time: {round(time.time() - time_start, 4)} seconds")

def data_generator():
    """Coordinate data generation"""
    # Setting up parser and saving console utility parameters
    parser = setup_parser()
    args_dict = save_console_utility_parameters(parser)

    # Checking if console utility arguments are valid
    check_args_dict(args_dict)

    # Setting path to save output files
    path_to_save_files = set_path_to_save_files(args_dict["path_to_save_files"])

    # Deleting all files in path_to_save_files that match file_name if needed
    delete_files_in_save_path(path_to_save_files, args_dict["file_name"], args_dict["clear_path"])

    # Reading data schema
    data_schema = read_data_schema(args_dict["data_schema"])

    # Generating file names
    file_names = gen_file_names(args_dict["files_count"], args_dict["file_name"], args_dict["file_prefix"], path_to_save_files)

    # Checking number of processes
    args_dict["multiprocessing"] = check_number_of_processes(args_dict["multiprocessing"])

    # Checking number of files
    check_number_of_files(args_dict["files_count"])

    # Validating data schema
    validate_schema(data_schema)

    # Generate files
    generate_json_files_all(file_names,
                            data_schema,
                            args_dict["multiprocessing"],
                            args_dict["data_lines"],
                            args_dict["files_count"],
                            path_to_save_files)


if __name__ == '__main__':
    data_generator()
