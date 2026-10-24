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

## Problem statement
The full assignment text wasn't saved in this folder. The class notes marked one topic as the assignment:

- **Operator precedence (BODMAS):** work out the order in which Python evaluates the operators in an expression, and how to control that order.

## Approach
Operator precedence is answered in section 3.7 of the class notebook:

1. **Precedence table:** every operator ranked from highest to lowest: `()` → `**` → unary `+ - ~` → `* / // %` → `+ -` → shifts → `&` → `^` → `|` → comparisons, `is`, `in` → `not` → `and` → `or`.
2. **Same-level operators:** evaluated left to right, except `**`, which goes right to left.
3. **Assignment comes last:** Python evaluates the whole right-hand side before storing the result.
4. **Worked examples, step by step:** `2 + 3 * 4`, `(2 + 3) * 4`, `2 ** 3 ** 2`, `-2 ** 2`, and an expression mixing arithmetic, comparison and logical operators.

## How to run
Open the class notebook in VS Code or Jupyter and run the cells from top to bottom:

```bash
jupyter notebook modules/01-python-linux/notebooks/01_variables_datatype.ipynb
```

Run the tests (currently a placeholder):

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
- **List:** ordered and mutable. **Tuple:** ordered and immutable. **Set:** unordered, with unique items.

## Open questions
