"""Relative paths depend on where you run python from, not where the script is.

Run this twice and compare the output (see 02_os_and_paths.ipynb, section 8):
    python Assignment/s06-python-3/paths_demo.py            (from the repo root)
    cd Assignment/s06-python-3 && python paths_demo.py      (from this folder)
"""

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = "Assignement.txt"                        # a file that sits next to this script
script_based_path = os.path.join(script_dir, "Assignement.txt")

print("cwd (where you ran python from)  :", os.getcwd())
print("script folder (where this file is):", script_dir)
print()
print("relative path resolves to    :", os.path.abspath(relative_path))
print("  exists?", os.path.exists(relative_path))
print("script-based path resolves to:", script_based_path)
print("  exists?", os.path.exists(script_based_path))
