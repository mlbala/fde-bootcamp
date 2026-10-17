# Session 05: Python 2 and Understanding Hash
**Date:** 2026-10-17
**Module:** 01 - Python & Linux Foundations
**Status:** In progress

## Problem statement
Build a complete understanding of how hashing works: what a hash function is, how a hash table (Python `dict`/`set`) uses it to store and look up data, and why it gives fast lookups.

## Approach
1. **What a hash is:** a function that maps any input to a fixed-size integer. The same input always gives the same output, and different inputs should rarely collide.
2. **Python's `hash()`:** try it on ints, strings and tuples; see why strings vary between runs (hash randomization) and why mutable types such as `list` are unhashable.
3. **How a hash table works:** hash the key, take it modulo the number of buckets to get an index, and store the value there.
4. **Collisions:** when two keys land in the same bucket, see how they are resolved (chaining or open addressing) and how resizing keeps lookups fast.
5. **Build a small hash table from scratch** in `solution.py` with set, get and delete, and test it with `test_solution.py`.
6. **Explore it in a notebook** (to be created in this folder) to demo each step with examples.

## How to run
Open the notebook in VS Code or Jupyter:

```bash
jupyter notebook Assignment/s05-python-2-hash/understanding_hash.ipynb
```

Run the tests:

```bash
pytest Assignment/s05-python-2-hash
```

## Learnings

## Open questions
