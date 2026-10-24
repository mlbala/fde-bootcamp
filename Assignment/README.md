# Assignments

Assignments from the FDE Bootcamp, one folder per class session. Each folder holds the assignment as it was given in class, the notebooks and code that answer it, tests, and a README describing the approach and what was learned.

## Index

| Session | Date | Module | Topics | Status | Folder |
|---------|------|--------|--------|--------|--------|
| 04 | 2026-10-11 | 01 - Python & Linux | Python 1: variables, data types, operators, operator precedence, collections | Completed | [s04-python-1](s04-python-1/) |
| 05 | 2026-10-17 | 01 - Python & Linux | Python 2: hashing and hash tables, string formatting, control flow, function basics | Completed | [s05-python-2-hash](s05-python-2-hash/) |
| 06 | 2026-10-24 | 01 - Python & Linux | Python 3: exceptions, `os` and paths, file handling, OOP, comprehensions, built-ins, `lambda` | Completed | [s06-python-3](s06-python-3/) |

## What each session contains

### Session 04: Python 1
- **Assignment:** operator precedence (BODMAS), the order in which Python evaluates the operators in an expression.
- **Answer:** section 3.7 of the class notebook [01_variables_datatype.ipynb](../modules/01-python-linux/notebooks/01_variables_datatype.ipynb), which also covers variables, data types, all operator types, lists, tuples and sets.
- Details: [s04-python-1/README.md](s04-python-1/README.md)

### Session 05: Python 2
| Topic | Files |
|-------|-------|
| How hashing works, from `hash()` to collisions, resizing and `hashlib` | [understanding_hash.ipynb](s05-python-2-hash/understanding_hash.ipynb) |
| A hash table built from scratch, with 19 tests | [solution.py](s05-python-2-hash/solution.py), [test_solution.py](s05-python-2-hash/test_solution.py) |
| `str.format()`, f-strings, `%` and the format spec mini-language | [string_formatting.ipynb](s05-python-2-hash/string_formatting.ipynb) |
| `if`/`elif`/`else`, `for`, `while` and function basics | [control_flow.ipynb](s05-python-2-hash/control_flow.ipynb) |
| Class demos for `input()` and nested dictionaries | [input_demo.py](s05-python-2-hash/input_demo.py), [print_demo.py](s05-python-2-hash/print_demo.py) |

Details: [s05-python-2-hash/README.md](s05-python-2-hash/README.md)

### Session 06: Python 3
- **Assignment** ([Assignement.txt](s06-python-3/Assignement.txt)): Priority 1 is exception handling, the `os` library, file handling and OOP. Priority 2 is comprehensions, useful built-ins and `lambda`. Each topic is studied as: introduce → behind the scenes → function → return → how to use.

| Topic | Files |
|-------|-------|
| Exception handling | [01_exception_handling.ipynb](s06-python-3/01_exception_handling.ipynb) |
| The `os` module: working directory, relative vs absolute paths, listing folders | [02_os_and_paths.ipynb](s06-python-3/02_os_and_paths.ipynb), [paths_demo.py](s06-python-3/paths_demo.py) |
| File handling with exception handling, plus JSON | [03_file_handling.ipynb](s06-python-3/03_file_handling.ipynb) |
| OOP: class, object, constructor, methods, attributes, `self` | [04_oops.ipynb](s06-python-3/04_oops.ipynb) |
| List and dict comprehensions | [05_comprehensions.ipynb](s06-python-3/05_comprehensions.ipynb) |
| `lambda`, `any`, `all`, `map`, `filter`, `enumerate`, `zip`, `sorted` | [06_lambda_and_builtins.ipynb](s06-python-3/06_lambda_and_builtins.ipynb) |
| Mini project: an expense tracker using every topic above, with 23 tests | [solution.py](s06-python-3/solution.py), [test_solution.py](s06-python-3/test_solution.py) |
| Class demos: from repeated code to a function with `return` | [functions.py](s06-python-3/functions.py), [functions_2.py](s06-python-3/functions_2.py) |

Each notebook ends with practice exercises left empty for you to answer (29 in total).

Details: [s06-python-3/README.md](s06-python-3/README.md)

## Folder layout

Session folders follow this structure. (Session 04's assignment text wasn't saved, and session 06's is named `Assignement.txt`.)

```text
Assignment/
├── README.md                # this index
└── sNN-<topic>/
    ├── README.md            # problem statement, approach, how to run, learnings
    ├── assignment.txt       # the assignment as given in class
    ├── *.ipynb              # one notebook per topic
    ├── solution.py          # code for the assignment
    └── test_solution.py     # pytest tests for solution.py
```

Files that the notebooks or scripts create at run time go into a `practice_files/` folder inside the session folder. It's git-ignored.

## How to run

Install the dependencies from the repo root (this includes `jupyter` and `pytest`):

```bash
pip install -r requirements.txt
```

**Notebooks:** open them in VS Code or Jupyter and run the cells from top to bottom. Examples that fail on purpose are wrapped in `try` / `except`, so **Run All** works.

```bash
jupyter notebook Assignment/
```

**Tests:** run one session folder at a time:

```bash
pytest Assignment/s04-python-1
pytest Assignment/s05-python-2-hash
pytest Assignment/s06-python-3
```

Running `pytest Assignment` on everything at once fails during collection, because every folder has a `test_solution.py` and a `solution.py` with the same names.

## Adding a new session

1. Create a folder named `sNN-<topic>`, for example `s07-python-4`.
2. Save the assignment as given in class as `assignment.txt`.
3. Add the notebooks, `solution.py` and `test_solution.py`.
4. Write the folder's `README.md`: problem statement, approach, how to run, learnings, open questions.
5. Add a row to the [index](#index) above.
