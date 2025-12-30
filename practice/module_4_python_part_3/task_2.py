"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math
import types
import unittest


class OperationNotFoundException(Exception):
    pass

class TooManyArguments(Exception):
    pass

def math_calculate(function: str, *args):
    func = getattr(math, function)
    if isinstance(func, (types.BuiltinFunctionType, types.FunctionType)):
        if 1 <= len(args) <= 2:
            return func(*args)
        else:
            raise TooManyArguments("Too many arguments. Math function can take 1 or 2 arguments")

    raise OperationNotFoundException("Function not found")

"""
Write tests for math_calculate function
"""

import pytest

@pytest.mark.parametrize("settings, expected", [
    (('log', 1024, 2), 10.0),
    (('ceil', 10.7), 11.0)
])
def test_math_calculate(settings, expected):
    assert math_calculate(*settings) == expected