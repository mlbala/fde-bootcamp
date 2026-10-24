"""Session 06 project 2: a file organizer (topics 1-3: exceptions, os, file handling).

Sorts the files in a messy folder (like Downloads) into sub-folders by type,
and can undo everything it did.

Uses topics 1-3 of the session, on top of sessions 04-05:
- os, the main topic: getcwd, path.abspath, path.expanduser, path.join, listdir,
  path.isfile / isdir / exists, path.splitext, path.relpath, makedirs, rename, remove, rmdir
- File handling: a JSON log of every move, and "x" mode for the sample files
- Exception handling: a bad folder, a file that can't be moved, a missing or broken log,
  and finally to write the log even if something stops the loop

It doesn't use OOP, comprehensions, lambda or the session's built-ins yet (topics 4-7,
projects 3-4). So every function takes the folder it works on, and lists and dicts
are built with plain for loops.

Run it from anywhere:
    python Assignment/s06-python-3/project-2/file_organizer.py

It starts on a practice folder of sample files (practice_files/messy_downloads), so
it's safe to try. It always shows the plan and asks before moving anything.
"""

import json
import os

# Build the path from this file's location, not the cwd (see 02_os_and_paths.ipynb)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FOLDER = os.path.join(SCRIPT_DIR, "practice_files", "messy_downloads")
LOG_NAME = "organizer_log.json"
OTHER = "Other"

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code": [".py", ".ipynb", ".js", ".html", ".css", ".json", ".sh", ".sql"],
}

SAMPLE_FILES = [
    "holiday photo.jpg", "Screenshot 2026-10-20.PNG", "logo.svg",
    "resume.pdf", "notes.txt", "budget.xlsx", "marks.csv",
    "song.mp3", "lecture recording.mp4", "project backup.zip",
    "solution.py", "analysis.ipynb", "data.json",
    "README", "setup.exe",
]


class LogError(Exception):
    """The undo log isn't valid JSON, or has entries that don't make sense."""


def build_extension_table(categories):
    """Turn {category: [extensions]} round into {extension: category}, so finding a
    file's category is one dict lookup instead of searching every list."""
    table = {}
    for category, extensions in categories.items():
        for extension in extensions:
            table[extension] = category
    return table


EXTENSION_TO_CATEGORY = build_extension_table(CATEGORIES)


def category_for(filename):
    """Return the category of a file from its extension, ignoring case."""
    _, extension = os.path.splitext(filename)  # "photo.JPG" -> ("photo", ".JPG")
    return EXTENSION_TO_CATEGORY.get(extension.lower(), OTHER)


def unique_path(path):
    """Return path, or "name (1).ext", "name (2).ext", ... if that name is already taken."""
    root, extension = os.path.splitext(path)
    number = 1
    while os.path.exists(path):
        path = f"{root} ({number}){extension}"
        number += 1
    return path


def is_safe_relative_path(path):
    """True for a path like "Images/photo.jpg" that stays inside the folder."""
    if not isinstance(path, str) or path == "" or os.path.isabs(path):
        return False
    return os.path.normpath(path).split(os.sep)[0] != ".."  # "../x" would point outside


def is_valid_move(move):
    """A log entry must be [original name, new path], both inside the folder."""
    if not isinstance(move, list) or len(move) != 2:
        return False
    for path in move:
        if not is_safe_relative_path(path):
            return False
    return True


def open_folder(folder):
    """Return the full path of folder. Raises NotADirectoryError if it isn't a folder."""
    # abspath turns a relative path into a full one, starting from the current working directory
    folder = os.path.abspath(os.path.expanduser(folder))
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"not a folder: {folder}")
    return folder


def log_path(folder):
    return os.path.join(folder, LOG_NAME)


def list_files(folder):
    """Return the names of the files directly in the folder, leaving out
    sub-folders, hidden files and the log."""
    names = []
    for name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, name)) and not name.startswith(".") and name != LOG_NAME:
            names.append(name)
    names.sort()  # os.listdir() returns the names in no particular order
    return names


def make_plan(folder):
    """Return what organize() would do, as (file name, category) pairs. Nothing is moved."""
    plan = []
    for name in list_files(folder):
        plan.append((name, category_for(name)))
    return plan


def group_by_category(plan):
    """Turn [(name, category), ...] into {category: [names]}, in the order of CATEGORIES."""
    groups = {}
    for category in list(CATEGORIES) + [OTHER]:
        names = []
        for name, file_category in plan:
            if file_category == category:
                names.append(name)
        if names:
            groups[category] = names
    return groups


def read_log(folder):
    """Return the logged moves as [original name, new path] pairs, or [] if there's no log.
    Raises LogError if the log is broken."""
    try:
        with open(log_path(folder), encoding="utf-8") as f:
            moves = json.load(f)
    except FileNotFoundError:
        return []
    except ValueError as e:  # json.JSONDecodeError is a ValueError
        raise LogError(f"{LOG_NAME} is not valid JSON ({e})") from None

    if not isinstance(moves, list):
        raise LogError(f"{LOG_NAME} should hold a list of moves")
    for move in moves:
        if not is_valid_move(move):
            raise LogError(f"{LOG_NAME} has an entry that isn't an [original, new] pair inside the folder: {move!r}")
    return moves


def write_log(folder, moves):
    with open(log_path(folder), "w", encoding="utf-8") as f:
        json.dump(moves, f, indent=2)


def organize(folder):
    """Move every file into its category folder, and log each move so it can be undone.

    Returns two lists: the moves that worked, and an error message for each file that
    couldn't be moved. Raises LogError, before moving anything, if the log is broken.
    """
    log = read_log(folder)  # read first: if the log is broken, stop now while nothing has moved
    moved = []
    errors = []
    try:
        for name, category in make_plan(folder):
            try:
                target_folder = os.path.join(folder, category)
                os.makedirs(target_folder, exist_ok=True)
                # rename() would silently replace an existing file on macOS and Linux, so never let it
                target = unique_path(os.path.join(target_folder, name))
                os.rename(os.path.join(folder, name), target)
            except OSError as e:  # PermissionError, a file called "Images" in the way, ...
                errors.append(f"{name}: {e}")
            else:
                moved.append([name, os.path.relpath(target, folder)])  # "Images/photo.jpg"
    finally:
        # Runs even if something unexpected stops the loop, so every move that did happen is logged
        if moved:
            write_log(folder, log + moved)
    return moved, errors


def undo(folder):
    """Move every logged file back, newest first, then tidy up.

    Returns (how many files were moved back, error messages). Raises LogError if the
    log is broken.
    """
    moves = read_log(folder)
    restored = 0
    errors = []
    failed = []  # moves to keep in the log, so a later undo can try them again
    for original, new in moves[::-1]:  # [::-1] walks the list backwards: newest move first
        source = os.path.join(folder, new)
        target = unique_path(os.path.join(folder, original))  # a new file may have taken the name
        try:
            os.rename(source, target)
        except FileNotFoundError:
            errors.append(f"{new} is not there any more, skipped it")
        except OSError as e:
            errors.append(f"{new}: {e}")
            failed.append([original, new])
        else:
            restored += 1

    # Remove the category folders that are now empty (a set, so each one is checked once)
    used_folders = set()
    for original, new in moves:
        used_folders.add(os.path.dirname(new))
    for name in used_folders:
        path = os.path.join(folder, name)
        if name and os.path.isdir(path) and not os.listdir(path):
            os.rmdir(path)

    if failed:
        write_log(folder, failed[::-1])  # back in the order they were made
    elif os.path.exists(log_path(folder)):
        os.remove(log_path(folder))
    return restored, errors


def create_sample_files(folder=SAMPLE_FOLDER):
    """Fill folder with sample files to practise on. Returns how many were created."""
    os.makedirs(folder, exist_ok=True)
    created = 0
    for name in SAMPLE_FILES:
        try:
            with open(os.path.join(folder, name), "x", encoding="utf-8") as f:  # "x": never overwrite
                f.write(f"Sample file: {name}\n")
        except FileExistsError:
            continue
        created += 1
    return created


def print_groups(groups):
    for category, names in groups.items():
        print(f"{category} ({len(names)})")
        for name in names:
            print("  " + name)


def choose_folder():
    """Ask for a folder until a valid one is given. Returns its full path, or None to cancel."""
    print(f"Relative paths start from the current working directory: {os.getcwd()}")
    while True:
        path = input("Folder (empty to cancel): ").strip()
        if not path:
            return None
        try:
            return open_folder(path)
        except NotADirectoryError as e:
            print(" ", e)


MENU = """\
1. Create sample files     4. Undo
2. Preview                 5. Choose another folder
3. Organize                6. Quit"""


def main():
    os.makedirs(SAMPLE_FOLDER, exist_ok=True)
    folder = SAMPLE_FOLDER

    while True:
        print(f"\nFolder: {folder}")
        print(MENU)
        choice = input("Choose 1-6: ").strip()
        try:
            if choice == "1":
                created = create_sample_files()
                folder = SAMPLE_FOLDER  # sample files only ever go in the practice folder
                print(f"  Created {created} sample files in the practice folder.")

            elif choice == "2":
                groups = group_by_category(make_plan(folder))
                if groups:
                    print_groups(groups)
                else:
                    print("  Nothing to organize.")

            elif choice == "3":
                plan = make_plan(folder)
                if not plan:
                    print("  Nothing to organize.")
                    continue
                groups = group_by_category(plan)
                print_groups(groups)
                if OTHER in groups:
                    print(f"  ({OTHER}: no extension, or one that isn't in CATEGORIES)")
                if input(f"Move {len(plan)} files? (y/n): ").strip().lower() != "y":
                    print("  Nothing was moved.")
                    continue
                moved, errors = organize(folder)
                for error in errors:
                    print("  Could not move", error)
                print(f"  Moved {len(moved)} files. Choose 4 to undo.")

            elif choice == "4":
                restored, errors = undo(folder)
                for error in errors:
                    print(" ", error)
                if restored:
                    print(f"  Moved {restored} files back.")
                else:
                    print("  Nothing to undo.")

            elif choice == "5":
                new_folder = choose_folder()
                if new_folder is not None:  # None means "cancelled": keep the old folder
                    folder = new_folder

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Please enter a number from 1 to 6.")

        except LogError as e:
            print("  Error:", e)
            print("  Fix or delete the log file, then try again.")
        except OSError as e:  # e.g. the folder was deleted while the program was running
            print("  Error:", e)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl + C or Ctrl + D
        print("\nGoodbye!")
