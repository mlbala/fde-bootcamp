import ast
import os
import subprocess
import sys

import pytest

from atm import (
    DAILY_LIMIT,
    MAX_PIN_TRIES,
    AccountNotFoundError,
    ATMError,
    CardBlockedError,
    DailyLimitError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidPinError,
    WrongPinError,
    change_pin,
    check_pin,
    deposit,
    find_account,
    format_statement,
    new_accounts,
    parse_amount,
    withdraw,
)

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm.py")

# Topic 1 only: nothing from topics 2-7 (os, files, OOP, comprehensions, built-ins, lambda)
FORBIDDEN = {"import os", "With", "open()", "Class", "ListComp", "DictComp", "SetComp", "GeneratorExp", "Lambda",
             "any()", "all()", "map()", "filter()", "enumerate()", "zip()", "sorted()"}


def constructs_used(path):
    """The kinds of syntax and the built-ins a file uses. A class whose only job is to be an
    exception (its bases end in Error or Exception) counts as "ExceptionClass", not "Class"."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    used = set()
    for node in ast.walk(tree):
        used.add(type(node).__name__)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used.add(node.func.id + "()")
        if isinstance(node, ast.Import):
            used.update("import " + alias.name for alias in node.names)
        if isinstance(node, ast.ClassDef):
            is_exception = node.bases and all(
                isinstance(base, ast.Name) and base.id.endswith(("Error", "Exception")) for base in node.bases
            )
            used.add("ExceptionClass" if is_exception else "Class")
    return used


@pytest.fixture
def account():
    return new_accounts()["1001"]  # Bala, PIN 1234, balance 15,000


def test_uses_only_topic_1():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_every_custom_error_is_an_atm_error():
    for error in (AccountNotFoundError, WrongPinError, CardBlockedError, InvalidAmountError,
                  InsufficientFundsError, DailyLimitError, InvalidPinError):
        assert issubclass(error, ATMError)


def test_find_account():
    assert find_account(new_accounts(), " 1002 ")["name"] == "Kumar"
    with pytest.raises(AccountNotFoundError):
        find_account(new_accounts(), "9999")


def test_correct_pin_resets_the_wrong_pin_count(account):
    with pytest.raises(WrongPinError, match="2 tries left"):
        check_pin(account, "0000")
    check_pin(account, "1234")
    assert account["wrong_pins"] == 0


def test_card_is_blocked_after_too_many_wrong_pins(account):
    for _ in range(MAX_PIN_TRIES - 1):
        with pytest.raises(WrongPinError):
            check_pin(account, "0000")
    with pytest.raises(CardBlockedError):
        check_pin(account, "0000")
    with pytest.raises(CardBlockedError):  # even the right PIN is refused now
        check_pin(account, "1234")


@pytest.mark.parametrize("text, expected", [("500", 500.0), (" 1,500 ", 1500.0), ("99.5", 99.5)])
def test_parse_amount(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize("text", ["", "abc", "-5", "0", "nan", "inf", "10.005"])
def test_parse_amount_rejects_bad_amounts(text):
    with pytest.raises(InvalidAmountError):
        parse_amount(text)


def test_deposit(account):
    deposit(account, 2500.5)
    assert account["balance"] == 17500.5
    with pytest.raises(InvalidAmountError):
        deposit(account, 50_001)


def test_withdraw(account):
    withdraw(account, 5000)
    assert account["balance"] == 10_000
    assert account["withdrawn_today"] == 5000


@pytest.mark.parametrize("amount, error", [(150, InvalidAmountError), (15_100, InsufficientFundsError)])
def test_withdraw_errors_leave_the_balance_alone(account, amount, error):
    with pytest.raises(error):
        withdraw(account, amount)
    assert account["balance"] == 15_000


def test_daily_limit(account):
    account["balance"] = 100_000
    withdraw(account, DAILY_LIMIT - 1000)
    with pytest.raises(DailyLimitError, match="Rs 1,000 more"):
        withdraw(account, 2000)


def test_mini_statement(account):
    assert "No transactions yet." in format_statement(account)
    deposit(account, 1000)
    withdraw(account, 500)
    statement = format_statement(account)
    assert "Deposit      +1,000.00     16,000.00" in statement
    assert "Withdraw       -500.00     15,500.00" in statement


def test_change_pin(account):
    change_pin(account, "1234", "5678", "5678")
    check_pin(account, "5678")


@pytest.mark.parametrize(
    "old, new, again, error",
    [("0000", "5678", "5678", WrongPinError), ("1234", "56a8", "56a8", InvalidPinError),
     ("1234", "567", "567", InvalidPinError), ("1234", "5678", "5679", InvalidPinError),
     ("1234", "1234", "1234", InvalidPinError)],
)
def test_change_pin_errors(account, old, new, again, error):
    with pytest.raises(error):
        change_pin(account, old, new, again)


def test_a_whole_visit_to_the_atm():
    typed = ["y", "1001", "0000", "1234", "3", "150", "3", "500", "4", "6", "y", "42", "n"]
    result = subprocess.run(
        [sys.executable, SCRIPT], input="\n".join(typed) + "\n", capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    output = result.stdout
    assert "wrong PIN, 2 tries left" in output
    assert "Welcome, Bala!" in output
    assert "enter a multiple of 100" in output  # the error is shown, and the menu carries on
    assert "Please take your cash: Rs 500" in output
    assert "no account with number '42'" in output
    assert output.count("Please take your card.") == 2  # finally runs after both visits
    assert "ATM switched off." in output
