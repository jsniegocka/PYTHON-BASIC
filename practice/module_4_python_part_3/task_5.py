"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib.request import urlopen

def make_request(url: str) -> Tuple[int, str]:
    with urlopen(url) as response:
        status_code = response.status
        data = response.read()
        text = data.decode("utf-8")

    return status_code, text

if __name__ == '__main__':
    make_request('https://www.google.com')

"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""

import unittest
from unittest.mock import MagicMock, patch

class TestMakeRequest(unittest.TestCase):

    @patch('task_5.urlopen')
    def test_make_request_success(self, mock_urlopen):

        mock_response = MagicMock()
        mock_response.__enter__.return_value.status = 200
        mock_response.__enter__.return_value.read.return_value = b'some response text'

        mock_urlopen.return_value = mock_response

        status, text = make_request('https://www.google.com')

        assert status == 200
        assert text == 'some response text'
        mock_urlopen.assert_called_once_with('https://www.google.com')
