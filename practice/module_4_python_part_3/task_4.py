"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
from faker import Faker

def print_name_address(args: argparse.Namespace) -> None:
    fake = Faker()
    for i in range(args.number):
        new_dict = {}
        for u in args.fields:
            field, provider = u.split("--")[1].split("=")
            new_dict[field] = getattr(fake, provider)()
        print(new_dict)

def main():
    parser = argparse.ArgumentParser(description="Generate fake data")
    parser.add_argument("number", type=int, help="Number of generated instances")
    args, unknown = parser.parse_known_args()
    args.fields = unknown
    print_name_address(args)

if __name__ == "__main__":
    main()

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

from unittest.mock import Mock, patch

@patch("practice.module_4_python_part_3.task_4.Faker")
def test_print_name_address_mocked_faker(MockFaker):
    fake_instance = MockFaker.return_value
    fake_instance.name.side_effect = ["Alice Smith", "Bob Johnson"]
    fake_instance.address.side_effect = ["123 Main St\nCityville", "456 Elm St\nTownsville"]

    args = Mock()
    args.number = 2
    args.fields = ["--some_name=name", "--fake_address=address"]

    with patch("builtins.print") as mock_print:
        print_name_address(args)

        assert mock_print.call_count == 2

        first_output = mock_print.call_args_list[0][0][0]
        assert first_output == {
            "fake_address": "123 Main St\nCityville",
            "some_name": "Alice Smith"
        }

        second_output = mock_print.call_args_list[1][0][0]
        assert second_output == {
            "fake_address": "456 Elm St\nTownsville",
            "some_name": "Bob Johnson"
        }