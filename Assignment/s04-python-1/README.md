# Session 04: Python 1 (Variables, Data Types, Operators, Collections)
**Date:** 2026-10-11
**Module:** 01 - Python & Linux Foundations
**Status:** In progress

## Class notes
Everything taught in this session is in [01_variables_datatype.ipynb](../../modules/01-python-linux/notebooks/01_variables_datatype.ipynb):

| # | Topic | What's covered |
|---|-------|----------------|
| 1 | Variables | assigning with `=`, naming rules, `snake_case` |
| 2 | Data types | `int`, `float`, `complex`, `bool`, `str`, `None`, `type()`, mutable vs immutable (with `id()`) |
| 3 | Operators | arithmetic, comparison, logical, identity, membership, bitwise, operator precedence |
| 4 | Collections | lists and their methods, tuples (and the single-item comma), sets |

## Projects
One small program, in the same format as the later sessions' projects. Its folder has a `project.txt` (the brief: its level, the topics it practises and the ones it doesn't use yet, requirements, a sample run and stretch goals), the program, and its tests. The test file also reads the program's code and fails if it uses a topic from later on.

| Folder | Program | Topics used | What it practises | Tests |
|--------|---------|-------------|-------------------|-------|
| [project-1](project-1/) | About me, a profile made of variables: [about_me.py](project-1/about_me.py) | 1-3 | `str`, `int`, `float`, `bool` and `None` with `type()`; age, height and BMI sums; `+` and `*` on text; yes/no answers with comparisons and `and`/`or`/`not`; `is not None`; a new `id()` after `age = age + 1` | 38 |

Topics: **1** variables, **2** data types, **3** operators, **4** collections. Variables, data types and operators can't really be used apart, so project 1 covers topics 1-3 together, using only the simple operators. It uses no collections, and nothing from session 05: there's no `input()`, so your details are variables at the top of the program (change them and run it again), and there's no `if`, so yes/no answers are printed as `True` or `False`.

## Problem statement
The full assignment text wasn't saved in this folder. The class notes marked one topic as the assignment:

- **Operator precedence (BODMAS):** work out the order in which Python evaluates the operators in an expression, and how to control that order.

## Approach
Operator precedence is answered in section 3.7 of the class notebook:

1. **Precedence table:** every operator ranked from highest to lowest: `()` → `**` → unary `+ - ~` → `* / // %` → `+ -` → shifts → `&` → `^` → `|` → comparisons, `is`, `in` → `not` → `and` → `or`.
2. **Same-level operators:** evaluated left to right, except `**`, which goes right to left.
3. **Assignment comes last:** Python evaluates the whole right-hand side before storing the result.
4. **Worked examples, step by step:** `2 + 3 * 4`, `(2 + 3) * 4`, `2 ** 3 ** 2`, `-2 ** 2`, and an expression mixing arithmetic, comparison and logical operators.
5. **In a program:** [project 1](project-1/) works out a BMI as `weight_kg / height_m ** 2` (`**` runs before `/`), and prints what the answer would be with the brackets in the wrong place.

## How to run
Open the class notebook in VS Code or Jupyter and run the cells from top to bottom:

```bash
jupyter notebook modules/01-python-linux/notebooks/01_variables_datatype.ipynb
```

Run the project. To describe someone else, change the variables at the top of `about_me.py`:

```bash
python Assignment/s04-python-1/project-1/about_me.py
```

Run the tests (the project's tests, plus the placeholder `test_solution.py`):

```bash
pytest Assignment/s04-python-1
```

## To do
- [ ] Paste the full assignment text into the problem statement, if there was more than operator precedence.
- [ ] Replace the placeholder `solution.py` and `test_solution.py` with real work for the assignment.

## Learnings
- A variable is a **name that refers to a value**. Python works out the type from the value, and `type()` shows it.
- Names can't start with a digit or be a keyword. Use meaningful `snake_case` names.
- **Immutable** objects (`int`, `str`, `tuple`) are replaced by a new object when "changed". **Mutable** objects (`list`, `set`) change in place and keep the same `id()`.
- `==` compares **values**; `is` compares **identity** (use it mainly for `x is None`).
- Precedence works like BODMAS: `()` → `**` → `* / // %` → `+ -` → comparisons → `not` → `and` → `or`. When in doubt, add parentheses.
- `/` always returns a `float`, even when it divides exactly (`4 / 2` is `2.0`). `//` and `%` work as a pair: `//` gives the whole units and `%` what's left over, so `age // 10` is the decades and `age % 10` the extra years.
- The type follows the value: `21` is an `int`, but `"21"` is a `str`, so `21 + 21` is `42` while `"21" + "21"` is `"2121"`. Joining a `str` and an `int` with `+` is an error; `print()` with commas shows both.
- `True` acts like 1 and `False` like 0, so adding up `True`/`False` answers counts how many are `True`.
- **List:** ordered and mutable. **Tuple:** ordered and immutable. **Set:** unordered, with unique items.

## Open questions
