"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""
import re


def is_http_domain(domain: str) -> bool:
    if re.fullmatch(r"^https?://.*/?$", domain):
        return True
    return False

"""
write tests for is_http_domain function
"""
import pytest

def test_is_http_domain_http():
    assert is_http_domain('http://wikipedia.org') is True

def test_is_http_domain_https():
    assert is_http_domain('https://wikipedia.org') is True

def test_is_http_domain_endslash():
    assert is_http_domain('http://wikipedia.org/') is True

def test_is_http_domain_incorrect():
    assert is_http_domain('griddynamics.com') is False