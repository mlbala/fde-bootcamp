import ast
import os
from datetime import datetime

import pytest

from billing import (
    MAX_QUANTITY,
    WIDTH,
    add_to_cart,
    calculate_bill,
    discount_rate,
    format_catalog,
    format_receipt,
    parse_quantity,
    remove_from_cart,
)


SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing.py")

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


@pytest.fixture
def cart():
    return {"A1": 2, "B1": 3, "D2": 1}  # 1,090 + 198 + 100 = 1,388


@pytest.mark.parametrize(
    "subtotal, expected",
    [(0, 0.0), (999.99, 0.0), (1000, 0.02), (1999, 0.02), (2000, 0.05), (4999, 0.05), (5000, 0.10), (90000, 0.10)],
)
def test_discount_rate_slabs(subtotal, expected):
    assert discount_rate(subtotal) == expected


@pytest.mark.parametrize("text, expected", [("1", 1), (" 12 ", 12), ("99", 99)])
def test_parse_quantity_valid(text, expected):
    assert parse_quantity(text) == (expected, None)


@pytest.mark.parametrize("text", ["", "abc", "1.5", "-2", "0", "100", "²"])
def test_parse_quantity_invalid(text):
    quantity, error = parse_quantity(text)
    assert quantity is None
    assert error


def test_add_to_cart_is_case_insensitive_and_adds_up():
    cart = {}
    assert add_to_cart(cart, " a1 ", 2) is None
    assert add_to_cart(cart, "A1", 3) is None
    assert cart == {"A1": 5}


def test_add_unknown_product():
    cart = {}
    assert "no product" in add_to_cart(cart, "Z9", 1)
    assert cart == {}


def test_add_more_than_max_quantity():
    cart = {"A1": MAX_QUANTITY}
    assert "at most" in add_to_cart(cart, "A1", 1)
    assert cart == {"A1": MAX_QUANTITY}


def test_remove_from_cart(cart):
    assert remove_from_cart(cart, "b1") is None
    assert "B1" not in cart
    assert "not in the cart" in remove_from_cart(cart, "B1")


def test_calculate_bill(cart):
    assert calculate_bill(cart) == {
        "items": 6,
        "subtotal": 1388.0,
        "rate": 0.02,
        "discount": 27.76,
        "tax": 68.01,
        "total": 1428.25,
    }


def test_bill_lines_add_up_to_the_total():
    bill = calculate_bill({"A3": 7, "B2": 3, "C2": 11})
    assert bill["subtotal"] - bill["discount"] + bill["tax"] == pytest.approx(bill["total"])


def test_empty_cart_bill():
    assert calculate_bill({})["total"] == 0


def test_receipt(cart):
    receipt = format_receipt(cart, "Bala", datetime(2026, 10, 24, 18, 30), 7)
    assert "24-10-2026 18:30   Bill #0007" in receipt
    assert "Customer: Bala" in receipt
    assert "Basmati rice 5kg            2   545.00  1,090.00" in receipt
    assert "Discount (2%)" in receipt
    assert "Rs 1,428.25" in receipt
    assert "6 items | You saved Rs 27.76 | Thank you!" in receipt
    assert all(len(line) <= WIDTH for line in receipt.splitlines())


def test_receipt_without_discount_has_no_discount_line():
    receipt = format_receipt({"B1": 1}, "Guest", datetime(2026, 1, 1), 1)
    assert "Discount" not in receipt


def test_catalog_lists_every_product():
    assert format_catalog().count("\n") == 10  # a header plus 10 products
