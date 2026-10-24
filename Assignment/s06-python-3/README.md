# Session 06: Python 3 (Exceptions, OS, Files, OOP, Comprehensions, Built-ins)
**Date:** 2026-10-24
**Module:** 01 - Python & Linux Foundations
**Status:** In progress

## Problem statement
From [Assignement.txt](Assignement.txt), as given in class:

**Priority 1**
- Exception handling
- OS library: `os.path.join`, `os.getcwd`, `os.listdir`, relative path vs full path
- File handling, practised together with exception handling
- OOP: class, object, constructor, methods, attributes, `self`

**Priority 2**
- Comprehensions: list and dict
- Useful built-ins: `any()`, `all()`, `map()`, `filter()`, `enumerate()`, `zip()`, `sorted()`
- `lambda`

**How to study each topic** (the note at the end of the assignment): introduce → behind the scenes → function → return → how to use.

## Today's assignments
| # | Priority | Topic | File |
|---|----------|-------|------|
| 1 | 1 | Exception handling | [01_exception_handling.ipynb](01_exception_handling.ipynb) |
| 2 | 1 | `os` library: `getcwd`, `path.join`, `listdir`, relative vs full paths | [02_os_and_paths.ipynb](02_os_and_paths.ipynb) |
| 3 | 1 | File handling, practised with exception handling | [03_file_handling.ipynb](03_file_handling.ipynb) |
| 4 | 1 | OOP: class, object, constructor, methods, attributes, `self` | [04_oops.ipynb](04_oops.ipynb) |
| 5 | 2 | List and dict comprehensions | [05_comprehensions.ipynb](05_comprehensions.ipynb) |
| 6 | 2 | `lambda`, `any`, `all`, `map`, `filter`, `enumerate`, `zip`, `sorted` | [06_lambda_and_builtins.ipynb](06_lambda_and_builtins.ipynb) |
| 7 | All | Mini project: an expense tracker that uses every topic above | [solution.py](solution.py), [test_solution.py](test_solution.py) |

Supporting files:
- [functions.py](functions.py): class demo. The same price × quantity calculation written out twice, to show the problem with repeated code.
- [functions_2.py](functions_2.py): class demo. The same calculation as `calculate_total(price, quantity)` with `return`, showing parameters vs arguments.
- [paths_demo.py](paths_demo.py): shows that a relative path depends on where you run `python` from, not where the script is.
- [.gitignore](.gitignore): keeps the `practice_files/` folder out of git.

## Approach
One notebook per topic, in the order of the assignment. Each one builds on the ones before it: file handling uses exceptions and `os`, the OOP examples raise exceptions, and the mini project uses everything.

Every concept follows the same pattern, taken from the assignment's note:

1. **What it is:** introduce the idea
2. **Behind the scenes:** what Python actually does
3. **Syntax:** the function or statement, and its parameters
4. **Returns:** what you get back
5. **How to use:** runnable examples and common mistakes, then practice exercises at the end of the notebook

Examples that fail on purpose are wrapped in `try` / `except`, so **Run All** works from top to bottom.

### 1. Exception handling ([01_exception_handling.ipynb](01_exception_handling.ipynb))
- **What an exception is,** and how to read a traceback.
- **`try` / `except`,** and catching the right exception: being specific, several `except` blocks, one block for several exceptions, the exception object (`as e`), the exception family tree (`LookupError` above `KeyError` and `IndexError`), and why catching everything is risky.
- **`else` and `finally`:** code for "no error happened" and code that always runs.
- **`raise`,** how exceptions travel up through function calls, and a custom `InsufficientBalanceError`.
- **Best practices,** then 4 practice exercises.

### 2. The `os` module and paths ([02_os_and_paths.ipynb](02_os_and_paths.ipynb))
- **The current working directory:** `os.getcwd()` and `os.chdir()`.
- **Absolute vs relative paths:** `os.path.abspath()`, `os.path.isabs()`.
- **Building paths** with `os.path.join()`, so they work on Windows, macOS and Linux.
- **Inspecting paths:** `exists`, `isfile`, `isdir`, `basename`, `dirname`, `split`, `splitext`, `getsize`.
- **Listing a folder** with `os.listdir()`.
- **Creating, renaming and removing:** `mkdir`, `makedirs`, `rename`, `remove`, `rmdir`.
- **Paths in `.py` scripts:** relative paths follow the cwd, not the script, so build them from `__file__` (see [paths_demo.py](paths_demo.py)). Ends with a note on `pathlib`, then 4 practice exercises.

### 3. File handling with exception handling ([03_file_handling.ipynb](03_file_handling.ipynb))
- **Behind the scenes:** what a file object is, and why files must be closed.
- **`open()` and file modes:** `"r"`, `"w"`, `"a"`, `"x"` and binary `"b"`.
- **Writing, reading and appending:** `write()`, `read()`, `readline()`, `readlines()`, and looping over a file line by line.
- **The `with` statement,** which closes the file even when an error happens.
- **File handling + exception handling:** a file that might not exist, several file errors, `"x"` mode so nothing is overwritten by accident, and bad data inside a file.
- **Structured data:** CSV-style text, and JSON with `json.dump()` / `json.load()`. Then 5 practice exercises.

### 4. OOP ([04_oops.ipynb](04_oops.ipynb))
- **Why OOP,** then class vs object.
- **The constructor** `__init__`, and what `self` really is behind the scenes.
- **Attributes:** instance attributes vs class attributes.
- **Methods,** and printing objects nicely with `__str__`.
- **Putting it together:** a `BankAccount` class with deposits, withdrawals and a statement. It raises `ValueError` for bad amounts and a custom `InsufficientFundsError` when you try to withdraw more than the balance. Then a summary and 5 practice exercises.

### 5. Comprehensions ([05_comprehensions.ipynb](05_comprehensions.ipynb))
- **What a comprehension is,** and the `for` loop it replaces.
- **List comprehensions,** filtering with `if`, and transforming with `if` / `else`.
- **Dict comprehensions,** plus set comprehensions and generator expressions as a bonus.
- **Nested comprehensions,** and when **not** to use a comprehension. Then 5 practice exercises.

### 6. `lambda` and useful built-ins ([06_lambda_and_builtins.ipynb](06_lambda_and_builtins.ipynb))
- **`lambda`:** one-line anonymous functions.
- **`enumerate()`, `zip()`, `map()`, `filter()`, `any()`, `all()` and `sorted()`,** each with its syntax, what it returns, and examples.
- **Putting it together,** a cheat sheet, then 6 practice exercises.

### 7. Mini project: expense tracker ([solution.py](solution.py))
A text menu for tracking expenses: **1** add, **2** list, **3** summary by category, **4** top 3, **5** save and quit.

| Topic | Where it's used |
|-------|-----------------|
| OOP | An `Expense` class that validates and cleans its fields, and an `ExpenseTracker` class with `add`, `total`, `total_by_category`, `in_category`, `largest`, `save` and `load` |
| Exception handling | A custom `InvalidExpenseError` for an empty description or category, commas, or an amount that isn't a positive number. The menu uses `try` / `except` / `else`. A missing file on the first run, an `OSError` when saving, and Ctrl + C / Ctrl + D are all handled |
| File handling | Saves to and loads from a CSV-style text file; bad lines are skipped with a warning |
| `os` | The file path is built from `__file__`, so it works from any folder; `os.makedirs` creates `practice_files/` |
| Comprehensions and built-ins | `sum()`, a set and dict comprehension for the category totals, `sorted(key=lambda ...)` for the top 3, and `enumerate()` for the numbered list |

[test_solution.py](test_solution.py) has **23 tests**. They cover field cleaning, invalid amounts and text, parsing a line, the totals and filters, the top 3, a save-and-load round trip, creating a missing folder, a missing file, and skipping bad lines. The file tests use pytest's `tmp_path`, so they never touch the real data file.

## How to run
Open the notebooks in VS Code or Jupyter and run the cells from top to bottom. They are saved without outputs, so run them to see the results:

```bash
jupyter notebook Assignment/s06-python-3/
```

Files created by the notebooks and the mini project go into `practice_files/` next to them. That folder is git-ignored, so it's safe to experiment and safe to delete.

Run the mini project:

```bash
python Assignment/s06-python-3/solution.py
```

Run the tests:

```bash
pytest Assignment/s06-python-3
```

See relative vs absolute paths in action (compare the two outputs):

```bash
python Assignment/s06-python-3/paths_demo.py
cd Assignment/s06-python-3 && python paths_demo.py
```

## To do
- [ ] **Practice exercises:** each notebook ends with a Practice section whose exercise cells are empty, ready for your answers. There are 29 in total: 4 in exceptions, 4 in `os`, 5 in files, 5 in OOP, 5 in comprehensions and 6 in built-ins.

## Learnings
- **Exceptions:** catch the most specific exception you can, and keep the `try` block small. `else` runs only when nothing went wrong, and `finally` always runs. Use `raise` in your own code to report bad input instead of returning a strange value.
- **Paths:** a relative path is relative to the current working directory, not to the script. Build paths with `os.path.join`, starting from `os.path.dirname(os.path.abspath(__file__))` when a script needs a file next to it.
- **Files:** always open files with `with` and `encoding="utf-8"`. `"w"` wipes the file, `"a"` adds to the end, and `"x"` refuses to overwrite. Expect `FileNotFoundError` and bad lines, and handle them.
- **OOP:** a class is the blueprint and an object is one thing built from it. `__init__` sets up each new object, and `self` is that object, passed in automatically when you call a method.
- **Comprehensions:** `[expr for item in items if condition]` replaces a loop that appends to a list. Use a normal loop when the logic needs more than one line or `try` / `except`.
- **Built-ins:** `map`, `filter` and `zip` return lazy iterators (wrap them in `list()` to see the values), `sorted` returns a new list, and `key=lambda ...` controls how items are compared.

## Open questions
