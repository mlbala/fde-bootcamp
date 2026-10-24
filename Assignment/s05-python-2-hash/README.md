# Session 05: Python 2 (Hash, String Formatting, Control Flow)
**Date:** 2026-10-17
**Module:** 01 - Python & Linux Foundations
**Status:** In progress

## Class notes
The session's class notebook is [02_collection_string_operations.ipynb](../../modules/01-python-linux/notebooks/02_collection_string_operations.ipynb). It covers sets, dictionaries, type casting, input and output, references and copying, and strings.

## Today's assignments
From [assignment.txt](assignment.txt):

| # | Topic | File |
|---|-------|------|
| 1 | Learn or research about hash | [understanding_hash.ipynb](understanding_hash.ipynb) |
| 1 | A hash table built from scratch, with tests | [solution.py](solution.py), [test_solution.py](test_solution.py) |
| 2 | `str.format()` and string formatting (optional) | [string_formatting.ipynb](string_formatting.ipynb) |
| 3 | `if`/`elif`/`else`, `for` and `while` loops, and function basics | [control_flow.ipynb](control_flow.ipynb) |

Every notebook follows the same pattern: **what it is → behind the scenes → syntax → returns → how to use**, and ends with practice exercises and worked solutions. Examples that fail on purpose are wrapped in `try` / `except`, so **Run All** works from top to bottom.

Class demo scripts:
- [input_demo.py](input_demo.py): `input()` always returns a string, so convert it with `float()` before adding two numbers.
- [print_demo.py](print_demo.py): reading one record from a nested dictionary with `.get()`.

## Projects
Five small programs that follow the order the topics are taught in: each project uses only the topics up to its own, plus sessions 04-05. Each folder has a `project.txt` (the brief: its level, the topics it practises and the ones it doesn't use yet, requirements, a sample run and stretch goals), the program, and its tests. Every test file also reads the program's code and fails if it uses a topic from later on.

| Folder | Program | Topics used | What it practises | Tests |
|--------|---------|-------------|-------------------|-------|
| [project-1](project-1/) | Secure sign-up and log-in: [secure_signup.py](project-1/secure_signup.py) | 1 | Salted `hashlib.pbkdf2_hmac`, a dict as the user store, `hash()` and buckets | 5 |
| [project-2](project-2/) | Report card: [report_card.py](project-2/report_card.py) | 1-2 | A `str.format()` template filled with `**`, alignment, `.2f`, `%`, dates; a SHA-256 verification code | 5 |
| [project-3](project-3/) | Calculator: [calculator.py](project-3/calculator.py) | 1-3 | Functions that return `(result, error)`, `if`/`elif` checks for division by zero and overflow, `while` loops that ask again | 50 |
| [project-4](project-4/) | Login system: [login_system.py](project-4/login_system.py) | 1-3 | Project 1 with a menu, password rules checked with a `for` loop, and account locking | 23 |
| [project-5](project-5/) | Supermarket billing: [billing.py](project-5/billing.py) | 1-3 | A receipt with any number of lines, discount slabs with `if`/`elif`, `cart.copy()` before `cart.clear()` | 29 |

Topics: **1** hash, **2** string formatting, **3** `if`/`elif`/`else`, `for`, `while` and function basics. Projects 1 and 2 come before topic 3, so they have no `if`, loops or `def`: they run from top to bottom, and a dict lookup such as `{True: "PASS", False: "FAIL"}[mark >= 40]` does the job of an `if`. None of the five uses session 06 topics (`try`/`except`, files, classes, comprehensions, `lambda`, `sorted()` and the other built-ins), so projects 3-5 check every input with `if` before using it.

## Problem statement
1. **Hash:** understand how hashing works: what a hash function is, how a hash table (Python's `dict` and `set`) uses one to store and find data, and why that makes lookups fast.
2. **String formatting (optional):** learn `str.format()` alongside the other ways of building strings from values.
3. **Control flow and functions:** `if`/`elif`/`else`, `for` and `while` loops, and the basics of functions.

## Approach
### 1. Hash ([understanding_hash.ipynb](understanding_hash.ipynb), [solution.py](solution.py))
1. **What a hash is:** a toy hash that adds up character codes. It shows that the same input always gives the same output, and that different inputs can collide (`"cat"` and `"act"`). A second, polynomial hash fixes the anagram collisions.
2. **Python's `hash()`:** tried on ints, floats and tuples. `1`, `1.0` and `True` share a hash, so they are one dict key. String hashes change between runs (hash randomization, shown by starting fresh Python processes).
3. **Hashable vs unhashable:** lists, dicts and sets are unhashable because they can change. Convert to a tuple or `frozenset` to use them as keys.
4. **How a hash table works:** `hash(key) % number_of_buckets` gives the bucket index. Built first with plain lists and two functions, `put()` and `lookup()`.
5. **Collisions:** chaining (a list per bucket) compared with open addressing (linear probing, the idea CPython uses).
6. **Load factor and resizing:** watching a real `dict` grow with `sys.getsizeof`.
7. **`HashTable` in `solution.py`:** `set`, `get`, `delete`, `in`, `len`, `items`, `show` and dict-style `[]` syntax. It uses chaining and doubles its buckets when it's more than 75% full. `test_solution.py` has 19 tests, including a comparison against a real `dict` after hundreds of operations.
8. **Why lookups are fast:** a `timeit` comparison of `in` on a list (O(n), checks every item) against a set and a dict (O(1) on average, jumps straight to the bucket).
9. **Cryptographic hashes:** `hashlib.sha256`, the avalanche effect, file integrity checks, Git commit IDs, and salted password hashing.
10. **Exercises:** word frequency, finding duplicates, two sum, and grouping anagrams.

### 2. String formatting ([string_formatting.ipynb](string_formatting.ipynb))
- **`str.format()` first:** positional, indexed and named placeholders, reusable templates filled from a dict with `**`, and `{0[key]}` access.
- **The other styles:** f-strings (including the `{name=}` debug form) and old-style `%` formatting.
- **The format spec mini-language:** precision, rounding, thousands separator, percent, binary/hex/octal, zero padding, scientific notation, alignment and fill.
- **Dates, dynamic widths and escaping braces,** then common mistakes and when to use which style.
- **Exercises:** a receipt, a report card, a mail merge, and a progress bar.

### 3. Control flow and function basics ([control_flow.ipynb](control_flow.ipynb))
- **`if`/`elif`/`else`:** a grading function, why order matters, a leap-year check, truthiness and the conditional expression.
- **`for` loops** over strings, `range()`, `enumerate()` and `dict.items()`, plus the accumulator pattern (totals, maximums, new lists).
- **`while` loops:** the Collatz sequence, taking a number apart digit by digit, and input validation.
- **`break`, `continue` and loop-`else`:** a prime number finder and a search.
- **Nested loops:** a multiplication table and a star pyramid.
- **Function basics:** `def`, parameters vs arguments, `print` vs `return`, default and keyword arguments, returning several values, early `return`, functions calling functions, and local variables.
- **Exercises:** FizzBuzz, a calculator, counting vowels, palindrome numbers, a guessing game, and a class report.

## How to run
Open the notebooks in VS Code or Jupyter and run the cells from top to bottom:

```bash
jupyter notebook Assignment/s05-python-2-hash/
```

Run the class demos (`input_demo.py` asks for two numbers):

```bash
python Assignment/s05-python-2-hash/input_demo.py
python Assignment/s05-python-2-hash/print_demo.py
```

Run the hash table demo:

```bash
python Assignment/s05-python-2-hash/solution.py
```

Run the projects:

```bash
python Assignment/s05-python-2-hash/project-1/secure_signup.py
python Assignment/s05-python-2-hash/project-2/report_card.py
python Assignment/s05-python-2-hash/project-3/calculator.py
python Assignment/s05-python-2-hash/project-4/login_system.py
python Assignment/s05-python-2-hash/project-5/billing.py
```

Run the tests (this includes the projects' tests):

```bash
pytest Assignment/s05-python-2-hash
```

## To do
- [x] **Function basics** (assignment item 3): section 6 of [control_flow.ipynb](control_flow.ipynb). Section 3 of the class notebook [03_ControlFlow_scope_of_variable.ipynb](../../modules/01-python-linux/notebooks/03_ControlFlow_scope_of_variable.ipynb) goes further.
- [x] **Hash table code:** the `HashTable` class now lives in `solution.py` (the notebook imports it), and `test_solution.py` tests `set`, `get`, `delete`, collisions and resizing.

## Learnings
- **Hashing:** a hash function turns a key into a number. `dict` and `set` use that number to jump straight to a bucket, which is why lookups are O(1) on average instead of O(n).
- **Keys must be hashable:** only immutable values (numbers, strings, tuples) can be dict keys or set items. If a key could change, its hash would change and the value would be lost.
- **Collisions are normal:** two keys can share a bucket. Chaining keeps both, and resizing keeps buckets short so lookups stay fast.
- **String hashes vary between runs** (hash randomization), so never save them or rely on them.
- **`hash()` vs `hashlib`:** `hash()` is for fast lookups inside one program. For hashes that must be secure or stay the same everywhere (checksums, Git IDs, passwords), use `hashlib.sha256`.
- **Formatting styles:** use f-strings by default, `str.format()` when the template is stored separately from the values, and `%` mainly in `logging`. The format spec is `{value:[fill][align][width][,][.precision][type]}`.
- **Control flow:** Python runs only the **first** branch whose condition is true. Empty values (`0`, `""`, `[]`, `None`) are falsy. A loop's `else` runs only if the loop finished without `break`.
- **Functions:** `return` gives a value back to the caller, while `print` only shows it (a function without `return` gives back `None`). Variables created inside a function are local to it.

## Open questions
