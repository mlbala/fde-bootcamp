import ast
import os

import pytest

from calculator import calculate, format_calculation, format_number, is_number, read_number

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculator.py")

# Session 05 topics only: nothing from session 06 yet
FORBIDDEN = {"Try", "ClassDef", "With", "open()", "ListComp", "DictComp", "SetComp", "GeneratorExp", "Lambda",
             "any()", "all()", "map()", "filter()", "enumerate()", "zip()", "sorted()"}


def constructs_used(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    used = set()
    for node in ast.walk(tree):
        used.add(type(node).__name__)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used.add(node.func.id + "()")
    return used


def test_uses_only_session_05_topics():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


@pytest.mark.parametrize("text", ["42", "-3.5", "+7", ".5", "5.", "  12  ", "0"])
def test_is_number_accepts_plain_numbers(text):
    assert is_number(text)


@pytest.mark.parametrize("text", ["", " ", "+", "-", ".", "abc", "1.2.3", "1 2", "12a", "--5", "1e5", "²"])
def test_is_number_rejects_everything_else(text):
    assert not is_number(text)


def test_read_number_converts_to_float():
    assert read_number(" -2.5 ") == (-2.5, None)


def test_read_number_ans_uses_previous_result():
    assert read_number("ANS", previous=99.0) == (99.0, None)


def test_read_number_ans_without_previous_result():
    number, error = read_number("ans")
    assert number is None
    assert "no previous answer" in error


@pytest.mark.parametrize("text", ["abc", "1" + "0" * 400])
def test_read_number_rejects_bad_or_huge_numbers(text):
    number, error = read_number(text)
    assert number is None
    assert error


@pytest.mark.parametrize(
    "a, operator, b, expected",
    [
        (7, "+", 3, 10),
        (7, "-", 3, 4),
        (7, "*", 3, 21),
        (7, "/", 2, 3.5),
        (7, "//", 2, 3),
        (7, "%", 3, 1),
        (2, "**", 10, 1024),
        (-8, "**", 3, -512),
        (9, "**", 0.5, 3),
    ],
)
def test_calculate_each_operator(a, operator, b, expected):
    assert calculate(a, operator, b) == (pytest.approx(expected), None)


@pytest.mark.parametrize(
    "a, operator, b",
    [
        (5, "/", 0),
        (5, "//", 0),
        (5, "%", 0),
        (0, "**", -1),
        (-8, "**", 0.5),
        (10, "**", 400),
        (-10, "**", 401),
        (1e300, "*", 1e300),
        (1e308, "+", 1e308),
        (5, "^", 2),
    ],
)
def test_calculate_returns_an_error_instead_of_crashing(a, operator, b):
    result, error = calculate(a, operator, b)
    assert result is None
    assert error


@pytest.mark.parametrize(
    "value, expected",
    [(2.0, "2"), (1234567.0, "1,234,567"), (0.1 + 0.2, "0.3"), (-0.0, "0"), (1 / 3, "0.3333333333")],
)
def test_format_number(value, expected):
    assert format_number(value) == expected


def test_format_calculation():
    assert format_calculation(1250.0, "*", 3.0, 3750.0) == "1,250 * 3 = 3,750"
