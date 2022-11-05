import pytest
import string

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def func(x):
    return x + 1


def is_palindrome(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.replace(" ", "")

    stack = []
    for char in text:
        stack.append(char)

    for char in text:
        c = stack.pop()
        if c != char:
            return False

    return True


def test_answer():
    assert func(3) == 4


def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 1


@pytest.mark.xfail
def test_alwaysfails():
    assert False


@pytest.mark.xfail
@pytest.mark.api
def test_api_access():
    assert False


@pytest.mark.parametrize(
    "palindrome", ["", "a", "Bob", "Never odd or even", "Do Geese see God?",]
)
def test_is_palindrome(palindrome):
    assert is_palindrome(palindrome)
