import ast
import hashlib
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_card.py")

# Topics 1-2 only: no control flow, functions, exceptions, classes or comprehensions
FORBIDDEN = {"If", "IfExp", "For", "While", "FunctionDef", "Lambda", "Try", "ClassDef",
             "ListComp", "DictComp", "SetComp", "GeneratorExp"}


def run(*lines):
    """Run the script with these lines typed in, and return what it printed."""
    result = subprocess.run(
        [sys.executable, SCRIPT], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def constructs_used(path):
    with open(path, encoding="utf-8") as f:
        return {type(node).__name__ for node in ast.walk(ast.parse(f.read()))}


def test_uses_only_topics_1_and_2():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_report_card():
    output = run(" asha ", "s05-017", "95", "88", "92", "79", "99")
    assert "Name : Asha" in output
    assert "Roll no:      S05-017" in output
    assert "Maths                       95       100        PASS" in output
    assert "Total                      453       500" in output
    assert "Average                  90.60" in output
    assert "Percentage               90.6%" in output
    assert "Grade                       A+" in output
    assert "Result                    PASS" in output
    card = output[output.index("=" * 52):]
    assert all(len(line) <= 52 for line in card.splitlines())  # the card fits in WIDTH


def test_failing_one_subject_fails_the_card_whatever_the_average():
    output = run("Gokul", "S05-020", "100", "100", "39", "100", "100")
    assert "English                     39       100        FAIL" in output
    assert "Grade                        F" in output
    assert "Result                    FAIL" in output


def test_grade_from_the_average():
    assert "Grade                        B" in run("A", "1", "70", "75", "72", "78", "71")  # average 73.2
    assert "Grade                       A+" in run("A", "1", "100", "100", "100", "100", "100")


def verification_code(output):
    return output.split("Verification code: ")[1].split()[0]


def test_verification_code_is_a_hash_of_the_details():
    output = run("Asha", "S05-017", "95", "88", "92", "79", "99")
    digest = hashlib.sha256(b"Asha|S05-017|95|88|92|79|99").hexdigest()[:12].upper()
    assert verification_code(output) == f"{digest[:4]}-{digest[4:8]}-{digest[8:]}"
    # One mark changed by one: a completely different code
    assert verification_code(run("Asha", "S05-017", "95", "88", "92", "79", "98")) != verification_code(output)
