import ast
import os

import pytest

from login_system import (
    LOGIN_FAILED,
    MAX_ATTEMPTS,
    change_password,
    format_users,
    hash_password,
    login,
    password_problems,
    register,
    username_problem,
)

GOOD_PASSWORD = "Secret#123"
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_system.py")

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
def users():
    users = {}
    assert register(users, "Bala", GOOD_PASSWORD) is None
    return users


def test_same_password_and_salt_give_the_same_hash():
    salt, first = hash_password(GOOD_PASSWORD)
    assert hash_password(GOOD_PASSWORD, salt) == (salt, first)


def test_same_password_with_new_salts_gives_different_hashes():
    assert hash_password(GOOD_PASSWORD)[1] != hash_password(GOOD_PASSWORD)[1]


def test_password_is_never_stored(users):
    record = users["bala"]
    assert set(record) == {"salt", "hash", "failed"}
    assert GOOD_PASSWORD.encode() not in record.values()


@pytest.mark.parametrize(
    "username, expected",
    [("ab", "3 to 15"), ("a" * 16, "3 to 15"), ("bad name", "letters, digits"), ("bala", "already taken")],
)
def test_username_problems(users, username, expected):
    assert expected in username_problem(username, users)


def test_valid_username_has_no_problem(users):
    assert username_problem("new_user_2", users) is None


def test_strong_password_has_no_problems():
    assert password_problems(GOOD_PASSWORD) == []


def test_weak_password_lists_every_problem():
    assert password_problems("abc") == [
        "needs at least 8 characters",
        "needs an upper case letter",
        "needs a digit",
        "needs a symbol such as ! @ # $",
    ]


def test_register_rejects_weak_password():
    users = {}
    assert register(users, "kumar", "password") == "password is too weak"
    assert users == {}


def test_register_is_case_insensitive(users):
    assert "already taken" in register(users, " BALA ", GOOD_PASSWORD)


def test_login_with_correct_password(users):
    assert login(users, "BALA", GOOD_PASSWORD) == (True, "welcome, bala!")


def test_unknown_user_and_wrong_password_look_the_same(users):
    assert login(users, "nobody", GOOD_PASSWORD) == (False, LOGIN_FAILED)
    assert login(users, "bala", "Wrong#123") == (False, LOGIN_FAILED)


def test_account_locks_after_too_many_wrong_passwords(users):
    for _ in range(MAX_ATTEMPTS):
        ok, message = login(users, "bala", "Wrong#123")
    assert not ok
    assert "locked" in message
    # Even the right password is refused now
    ok, message = login(users, "bala", GOOD_PASSWORD)
    assert not ok
    assert "locked" in message


def test_correct_password_resets_failed_count(users):
    login(users, "bala", "Wrong#123")
    login(users, "bala", GOOD_PASSWORD)
    assert users["bala"]["failed"] == 0


def test_change_password(users):
    old_salt = users["bala"]["salt"]
    assert change_password(users, "bala", GOOD_PASSWORD, "Newer$456") is None
    assert users["bala"]["salt"] != old_salt
    assert login(users, "bala", "Newer$456")[0]
    assert not login(users, "bala", GOOD_PASSWORD)[0]


@pytest.mark.parametrize(
    "old, new, expected",
    [
        ("Wrong#123", "Newer$456", LOGIN_FAILED),
        (GOOD_PASSWORD, GOOD_PASSWORD, "must be different"),
        (GOOD_PASSWORD, "weak", "too weak"),
    ],
)
def test_change_password_errors(users, old, new, expected):
    assert expected in change_password(users, "bala", old, new)


def test_format_users_shows_hash_prefix_not_password(users):
    table = format_users(users)
    assert users["bala"]["hash"].hex()[:12] in table
    assert GOOD_PASSWORD not in table
    assert "active" in table


def test_format_users_when_empty():
    assert format_users({}) == "No users yet."
