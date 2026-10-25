# Assignments

Assignments from the FDE Bootcamp, one folder per class session. Each folder holds the assignment as it was given in class, the notebooks and code that answer it, tests, and a README describing the approach and what was learned.

## Index

| Session | Date | Module | Topics | Status | Folder |
|---------|------|--------|--------|--------|--------|
| 04 | 2026-10-11 | 01 - Python & Linux | Python 1: variables, data types, operators, operator precedence, collections | Completed | [s04-python-1](s04-python-1/) |
| 05 | 2026-10-17 | 01 - Python & Linux | Python 2: hashing and hash tables, string formatting, control flow, function basics | Completed | [s05-python-2-hash](s05-python-2-hash/) |
| 06 | 2026-10-24 | 01 - Python & Linux | Python 3: exceptions, `os` and paths, file handling, OOP, comprehensions, built-ins, `lambda` | Completed | [s06-python-3](s06-python-3/) |

## Projects

Small programs that practise each session's topics. Within a session, projects follow the order the topics are taught, so the **Topics** column lists the session topics each project may use: each project adds the next topic and never uses a later one. Each one also uses the basics from earlier sessions.

| Session | Project | Program | Topics | Tests | Status | Folder |
|---------|---------|---------|--------|-------|--------|--------|
| 04 | 1 | About me: a profile made of variables ([about_me.py](s04-python-1/project-1/about_me.py)) | Variables, data types, operators | 38 | Completed | [s04-python-1/project-1](s04-python-1/project-1/) |
| 05 | 1 | Secure sign-up and log-in ([secure_signup.py](s05-python-2-hash/project-1/secure_signup.py)) | Hash | 5 | Completed | [s05-python-2-hash/project-1](s05-python-2-hash/project-1/) |
| 05 | 2 | Report card generator ([report_card.py](s05-python-2-hash/project-2/report_card.py)) | Hash, string formatting | 5 | Completed | [s05-python-2-hash/project-2](s05-python-2-hash/project-2/) |
| 05 | 3 | Calculator ([calculator.py](s05-python-2-hash/project-3/calculator.py)) | Hash, string formatting, control flow and functions | 50 | Completed | [s05-python-2-hash/project-3](s05-python-2-hash/project-3/) |
| 05 | 4 | Login system with hashed passwords ([login_system.py](s05-python-2-hash/project-4/login_system.py)) | Hash, string formatting, control flow and functions | 23 | Completed | [s05-python-2-hash/project-4](s05-python-2-hash/project-4/) |
| 05 | 5 | Supermarket billing ([billing.py](s05-python-2-hash/project-5/billing.py)) | Hash, string formatting, control flow and functions | 29 | Completed | [s05-python-2-hash/project-5](s05-python-2-hash/project-5/) |
| 06 | 1 | ATM machine ([atm.py](s06-python-3/project-1/atm.py)) | Exceptions | 28 | Completed | [s06-python-3/project-1](s06-python-3/project-1/) |
| 06 | 2 | File organizer with undo ([file_organizer.py](s06-python-3/project-2/file_organizer.py)) | Exceptions, `os`, file handling | 25 | Completed | [s06-python-3/project-2](s06-python-3/project-2/) |
| 06 | 3 | Library management system ([library.py](s06-python-3/project-3/library.py)) | Exceptions, `os`, file handling, OOP | 27 | Completed | [s06-python-3/project-3](s06-python-3/project-3/) |
| 06 | 4 | Student marks analyzer ([marks_analyzer.py](s06-python-3/project-4/marks_analyzer.py)) | All 7: exceptions, `os`, file handling, OOP, comprehensions, built-ins, `lambda` | 34 | Completed | [s06-python-3/project-4](s06-python-3/project-4/) |

Each project folder has a `project.txt` with the brief (level, requirements, a sample run and stretch goals), the program, and its tests. "Completed" means the program is written and all its tests pass.

## What each session contains

### Session 04: Python 1
- **Assignment:** operator precedence (BODMAS), the order in which Python evaluates the operators in an expression.
- **Answer:** section 3.7 of the class notebook [01_variables_datatype.ipynb](../modules/01-python-linux/notebooks/01_variables_datatype.ipynb), which also covers variables, data types, all operator types, lists, tuples and sets.
- **Project** ([project-1](s04-python-1/project-1/)): "about me", a profile made of variables. It shows each value's data type, does sums with the age, height and weight, joins text with `+`, and answers yes/no questions with comparison and logical operators. It has 38 tests.
- Details: [s04-python-1/README.md](s04-python-1/README.md)

### Session 05: Python 2
| Topic | Files |
|-------|-------|
| How hashing works, from `hash()` to collisions, resizing and `hashlib` | [understanding_hash.ipynb](s05-python-2-hash/understanding_hash.ipynb) |
| A hash table built from scratch, with 19 tests | [solution.py](s05-python-2-hash/solution.py), [test_solution.py](s05-python-2-hash/test_solution.py) |
| `str.format()`, f-strings, `%` and the format spec mini-language | [string_formatting.ipynb](s05-python-2-hash/string_formatting.ipynb) |
| `if`/`elif`/`else`, `for`, `while` and function basics | [control_flow.ipynb](s05-python-2-hash/control_flow.ipynb) |
| Class demos for `input()` and nested dictionaries | [input_demo.py](s05-python-2-hash/input_demo.py), [print_demo.py](s05-python-2-hash/print_demo.py) |
| Projects in topic order: secure sign-up (hash only), a report card (+ string formatting), then a calculator, a login system and a supermarket billing system (+ control flow and functions), with 112 tests | [project-1](s05-python-2-hash/project-1/), [project-2](s05-python-2-hash/project-2/), [project-3](s05-python-2-hash/project-3/), [project-4](s05-python-2-hash/project-4/), [project-5](s05-python-2-hash/project-5/) |

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
| Projects in topic order: an ATM (exceptions), a file organizer with undo (+ `os` and files), a library system (+ OOP), and a student marks analyzer (+ comprehensions, built-ins, `lambda`), with 114 tests | [project-1](s06-python-3/project-1/), [project-2](s06-python-3/project-2/), [project-3](s06-python-3/project-3/), [project-4](s06-python-3/project-4/) |

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
    ├── test_solution.py     # pytest tests for solution.py
    └── project-N/           # optional: small apps, numbered in the order of the session's topics
        ├── project.txt      # the brief: level, topics practised, requirements, sample run
        ├── <app>.py         # the app, e.g. calculator.py
        └── test_<app>.py    # pytest tests for the app
```

Projects follow the order the session's topics are taught in: project 1 uses only the first topic (or the first few, when they can't be used apart, like session 04's variables, data types and operators), and each project after it may add the next ones. A project never uses a topic that comes later (OOP isn't allowed in a project that comes before the OOP topic, for example), and its tests check this. Each project's files have their own names (not `solution.py`), so `pytest` on a session folder runs the project tests along with `test_solution.py`.

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
