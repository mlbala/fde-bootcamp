import ast
import contextlib
import io
import os
import subprocess
import sys

import pytest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about_me.py")

# Topics 1-3 only: no collections (topic 4), and nothing from sessions 05-06: dicts, indexing, imports,
# control flow, functions, string formatting, exceptions, classes or comprehensions
FORBIDDEN = {
    "List", "Tuple", "Set", "Dict", "Subscript", "Import", "ImportFrom",
    "If", "IfExp", "For", "While", "FunctionDef", "Lambda", "Try", "With", "ClassDef",
    "JoinedStr", "ListComp", "DictComp", "SetComp", "GeneratorExp",
}
# The only functions the class notebook uses on variables. No methods either: those come in session 05.
ALLOWED_CALLS = {"print", "type", "id"}


def run(**changes):
    """Run the script with some of the variables at its top changed, and return its variables and output."""
    with open(SCRIPT, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in changes:
            node.value = ast.Constant(changes.pop(node.targets[0].id))  # pop: only the first assignment changes
    assert not changes, "no such variable in the script: " + ", ".join(changes)
    variables = {}
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(ast.fix_missing_locations(tree), SCRIPT, "exec"), variables)
    return variables, output.getvalue()


def constructs_used(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    return {type(node).__name__ for node in ast.walk(tree)}


def functions_called(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called.add(node.func.id)
        elif isinstance(node, ast.Call):
            called.add("." + getattr(node.func, "attr", "?") + "()")
    return called


def test_uses_only_topics_1_to_3():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_calls_only_print_type_and_id():
    assert functions_called(SCRIPT) <= ALLOWED_CALLS


def test_runs_from_the_command_line():
    result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "Full name: Bala Kumar" in result.stdout


# ---- Step 1: variables and their data types ----

def test_shows_every_variable_with_its_type():
    _, output = run()
    assert "first_name = Bala <class 'str'>" in output
    assert "age        = 21 <class 'int'>" in output
    assert "height_m   = 1.75 <class 'float'>" in output
    assert "is_student = True <class 'bool'>" in output
    assert "nickname   = None <class 'NoneType'>" in output


def test_the_type_follows_the_value():
    _, output = run(age=21.5, nickname="Bala2")
    assert "age        = 21.5 <class 'float'>" in output
    assert "nickname   = Bala2 <class 'str'>" in output


# ---- Step 2: arithmetic ----

@pytest.mark.parametrize("age, months, days, birth_year, decades, extra_years", [
    (21, 252, 7665, 2005, 2, 1),
    (0, 0, 0, 2026, 0, 0),
    (9, 108, 3285, 2017, 0, 9),
    (10, 120, 3650, 2016, 1, 0),
    (45, 540, 16425, 1981, 4, 5),
])
def test_age_arithmetic(age, months, days, birth_year, decades, extra_years):
    variables, _ = run(age=age)
    assert variables["age_in_months"] == months
    assert variables["age_in_days"] == days
    assert variables["birth_year"] == birth_year
    assert (variables["decades"], variables["extra_years"]) == (decades, extra_years)


def test_height_in_cm_is_a_float():
    variables, output = run()
    assert variables["height_cm"] == 175.0
    assert type(variables["height_cm"]) is float
    assert "Height in cm: 175.0" in output


@pytest.mark.parametrize("weight, height, expected", [(68.5, 1.75, 22.367), (80, 2.0, 20.0), (50, 1.6, 19.531)])
def test_bmi_divides_by_height_squared(weight, height, expected):
    variables, _ = run(weight_kg=weight, height_m=height)
    assert variables["bmi"] == pytest.approx(expected, abs=0.001)
    assert type(variables["bmi"]) is float


def test_brackets_change_the_order():
    _, output = run(weight_kg=80, height_m=2.0)
    assert "BMI: 20.0 <- weight_kg / height_m ** 2" in output
    assert "(weight_kg / height_m) ** 2 would be 1600.0" in output


# ---- Step 3: text ----

def test_full_name_is_joined_with_a_space():
    variables, _ = run(first_name="Priya", last_name="Sharma")
    assert variables["full_name"] == "Priya Sharma"


def test_numbers_add_but_text_joins_and_repeats():
    _, output = run()
    assert "number + number = 42 <- adds" in output
    assert "text + text     = 2121 <- joins" in output
    assert "text * 3        = 212121 <- repeats" in output


# ---- Step 4: comparison and logical operators ----

@pytest.mark.parametrize("age, is_adult, is_teenager", [
    (12, False, False),
    (13, False, True),
    (17, False, True),
    (18, True, True),
    (19, True, True),
    (20, True, False),
])
def test_adult_and_teenager_at_the_edges(age, is_adult, is_teenager):
    variables, _ = run(age=age)
    assert variables["is_adult"] is is_adult
    assert variables["is_teenager"] is is_teenager


@pytest.mark.parametrize("age, is_citizen, can_vote", [(21, True, True), (21, False, False), (16, True, False)])
def test_can_vote_needs_both(age, is_citizen, can_vote):
    variables, _ = run(age=age, is_citizen=is_citizen)
    assert variables["can_vote"] is can_vote


@pytest.mark.parametrize("is_student, age, discount", [(True, 21, True), (True, 24, True), (True, 25, False), (False, 21, False)])
def test_student_discount_and_full_price(is_student, age, discount):
    variables, _ = run(is_student=is_student, age=age)
    assert variables["gets_student_discount"] is discount
    assert variables["pays_full_price"] is (not discount)


@pytest.mark.parametrize("weight, expected", [(73.9, False), (74, True), (85, True), (99.9, True), (100, False)])
def test_healthy_bmi_range(weight, expected):
    # with a height of 2.0 m, 74 kg is a BMI of exactly 18.5 (healthy) and 100 kg exactly 25 (not)
    variables, _ = run(weight_kg=weight, height_m=2.0)
    assert variables["healthy_bmi"] is expected


def test_true_counts_as_one():
    variables, output = run()
    assert variables["yes_count"] == 4
    assert "4 out of 4" in output
    variables, _ = run(age=16, is_student=False)  # not adult, can't vote, no discount, BMI still fine
    assert variables["yes_count"] == 1


# ---- Step 5: None, and changing a variable ----

def test_no_nickname_is_none():
    variables, output = run()
    assert variables["has_nickname"] is False
    assert "Has a nickname? False" in output
    variables, _ = run(nickname="Bala2")
    assert variables["has_nickname"] is True


def test_a_birthday_makes_a_new_int():
    variables, output = run()
    assert variables["age"] == 22
    assert "After a birthday, age is 22" in output
    assert "Same object as before? False" in output
