import ast
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secure_signup.py")

# Topic 1 only: no control flow, functions, string formatting, exceptions, classes or comprehensions
FORBIDDEN = {
    "If", "IfExp", "For", "While", "FunctionDef", "Lambda", "Try", "ClassDef",
    "JoinedStr", ".format()", "ListComp", "DictComp", "SetComp", "GeneratorExp",
}


def run(*lines):
    """Run the script with these lines typed in, and return what it printed."""
    result = subprocess.run(
        [sys.executable, SCRIPT], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def constructs_used(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    used = set()
    for node in ast.walk(tree):
        used.add(type(node).__name__)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format":
            used.add(".format()")
    return used


def test_uses_only_topic_1():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_correct_login():
    output = run("Bala", "Secret#123", " BALA ", "Secret#123")
    assert "Login successful. Welcome, bala!" in output


def test_wrong_password_and_unknown_user_get_the_same_message():
    assert "Invalid username or password." in run("bala", "Secret#123", "bala", "wrong")
    assert "Invalid username or password." in run("bala", "Secret#123", "nobody", "Secret#123")


def test_password_is_not_stored_and_salt_changes_the_hash():
    output = run("bala", "Secret#123", "bala", "Secret#123")
    assert "Fields stored: ['salt', 'hash']" in output
    assert "Hash length:     64 hex characters" in output
    assert "same salt -> same hash? True" in output
    assert "new salt  -> same hash? False" in output


def test_hash_table_lookups():
    output = run("admin", "x", "admin", "x")
    assert "'admin' in users: True" in output
    assert "'nobody' in users: False" in output
    assert "Is 'admin' a reserved name? True" in output
