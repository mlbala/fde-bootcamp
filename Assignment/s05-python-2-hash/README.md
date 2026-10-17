# Session 05: Python 2 (Hash, String Formatting, Control Flow)
**Date:** 2026-10-17
**Module:** 01 - Python & Linux Foundations
**Status:** In progress

## Today's assignments
| # | Topic | Notebook |
|---|-------|----------|
| 1 | Understanding hash | [understanding_hash.ipynb](understanding_hash.ipynb) |
| 2 | String formatting (f-strings, `.format()`, `%`, format spec) | [string_formatting.ipynb](string_formatting.ipynb) |
| 3 | `if`/`elif`/`else`, `for` and `while` loops | [control_flow.ipynb](control_flow.ipynb) |

## Problem statement (assignment 1: hash)
Build a complete understanding of how hashing works: what a hash function is, how a hash table (Python `dict`/`set`) uses it to store and look up data, and why it gives fast lookups.

## Approach
1. **What a hash is:** a function that maps any input to a fixed-size integer. The same input always gives the same output, and different inputs should rarely collide.
2. **Python's `hash()`:** try it on ints, strings and tuples; see why strings vary between runs (hash randomization) and why mutable types such as `list` are unhashable.
3. **How a hash table works:** hash the key, take it modulo the number of buckets to get an index, and store the value there.
4. **Collisions:** when two keys land in the same bucket, see how they are resolved (chaining or open addressing) and how resizing keeps lookups fast.
5. **Build a small hash table from scratch** in `solution.py` with set, get and delete, and test it with `test_solution.py`.
6. **Explore it in a notebook** (`understanding_hash.ipynb`) to demo each step with examples.

### Assignment 2: string formatting
Compare f-strings, `str.format()` and `%` formatting, then cover the format spec mini-language (precision, width, alignment, fill, separators, number bases, percent) and finish with a receipt exercise.

### Assignment 3: control flow
Cover `if`/`elif`/`else` (including truthiness and the conditional expression), `for` over iterables with `range` and `enumerate`, `while` loops, `break`/`continue`/loop-`else`, nested loops, and a FizzBuzz exercise.

## How to run
Open the notebook in VS Code or Jupyter:

```bash
jupyter notebook Assignment/s05-python-2-hash/
```

Run the tests:

```bash
pytest Assignment/s05-python-2-hash
```

## Learnings

## Open questions
