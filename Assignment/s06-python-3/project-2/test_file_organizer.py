import ast
import json
import os

import pytest

from file_organizer import (
    CATEGORIES,
    EXTENSION_TO_CATEGORY,
    LOG_NAME,
    SAMPLE_FILES,
    LogError,
    category_for,
    create_sample_files,
    group_by_category,
    list_files,
    make_plan,
    open_folder,
    organize,
    undo,
    unique_path,
)

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file_organizer.py")

# Topics 1-3 only: nothing from topics 4-7 (OOP, comprehensions, built-ins, lambda)
FORBIDDEN = {"Class", "ListComp", "DictComp", "SetComp", "GeneratorExp", "Lambda",
             "any()", "all()", "map()", "filter()", "enumerate()", "zip()", "sorted()"}


def constructs_used(path):
    """The kinds of syntax and the built-ins a file uses. A class whose only job is to be an
    exception (its bases end in Error or Exception) counts as "ExceptionClass", not "Class"."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    used = set()
    for node in ast.walk(tree):
        used.add(type(node).__name__)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used.add(node.func.id + "()")
        if isinstance(node, ast.ClassDef):
            is_exception = node.bases and all(
                isinstance(base, ast.Name) and base.id.endswith(("Error", "Exception")) for base in node.bases
            )
            used.add("ExceptionClass" if is_exception else "Class")
    return used


def make_files(folder, *names):
    for name in names:
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            f.write(name)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def folder(tmp_path):
    make_files(tmp_path, "photo.JPG", "cv.pdf", "song.mp3", "README")
    return str(tmp_path)


def test_uses_only_topics_1_to_3():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_no_extension_is_in_two_categories():
    assert len(EXTENSION_TO_CATEGORY) == sum(len(extensions) for extensions in CATEGORIES.values())


@pytest.mark.parametrize(
    "name, expected",
    [("photo.JPG", "Images"), ("cv.pdf", "Documents"), ("backup.tar.gz", "Archives"), ("README", "Other"), ("setup.exe", "Other")],
)
def test_category_for(name, expected):
    assert category_for(name) == expected


def test_missing_folder_raises(tmp_path):
    with pytest.raises(NotADirectoryError):
        open_folder(os.path.join(tmp_path, "nope"))


def test_relative_folder_becomes_absolute(folder, monkeypatch):
    monkeypatch.chdir(os.path.dirname(folder))
    assert open_folder(os.path.basename(folder)) == folder


def test_list_files_skips_folders_hidden_files_and_the_log(folder):
    os.mkdir(os.path.join(folder, "Images"))
    make_files(folder, ".DS_Store", LOG_NAME)
    assert list_files(folder) == ["README", "cv.pdf", "photo.JPG", "song.mp3"]


def test_plan_moves_nothing(folder):
    assert ("photo.JPG", "Images") in make_plan(folder)
    assert os.path.exists(os.path.join(folder, "photo.JPG"))


def test_group_by_category_follows_the_order_of_categories():
    plan = [("x", "Other"), ("b.png", "Images"), ("cv.pdf", "Documents"), ("a.png", "Images")]
    assert group_by_category(plan) == {"Images": ["b.png", "a.png"], "Documents": ["cv.pdf"], "Other": ["x"]}
    assert list(group_by_category(plan)) == ["Images", "Documents", "Other"]


def test_unique_path(tmp_path):
    make_files(tmp_path, "a.txt", "a (1).txt")
    assert unique_path(os.path.join(tmp_path, "a.txt")) == os.path.join(tmp_path, "a (2).txt")
    assert unique_path(os.path.join(tmp_path, "b.txt")) == os.path.join(tmp_path, "b.txt")


def test_organize_moves_files_and_logs_them(folder):
    moved, errors = organize(folder)
    assert errors == []
    assert len(moved) == 4
    assert read(os.path.join(folder, "Images", "photo.JPG")) == "photo.JPG"
    assert os.path.exists(os.path.join(folder, "Other", "README"))
    assert not os.path.exists(os.path.join(folder, "photo.JPG"))
    with open(os.path.join(folder, LOG_NAME), encoding="utf-8") as f:
        assert len(json.load(f)) == 4


def test_organize_never_overwrites(folder):
    os.mkdir(os.path.join(folder, "Images"))
    with open(os.path.join(folder, "Images", "photo.JPG"), "w", encoding="utf-8") as f:
        f.write("the old photo")
    organize(folder)
    assert read(os.path.join(folder, "Images", "photo.JPG")) == "the old photo"
    assert read(os.path.join(folder, "Images", "photo (1).JPG")) == "photo.JPG"


def test_a_file_that_cannot_be_moved_does_not_stop_the_rest(folder, monkeypatch):
    real_rename = os.rename

    def rename(source, target):  # pretend cv.pdf is locked by another program
        if source.endswith("cv.pdf"):
            raise PermissionError("permission denied")
        real_rename(source, target)

    monkeypatch.setattr(os, "rename", rename)
    moved, errors = organize(folder)
    assert errors == ["cv.pdf: permission denied"]
    assert len(moved) == 3
    assert os.path.exists(os.path.join(folder, "cv.pdf"))
    assert os.path.exists(os.path.join(folder, "Images", "photo.JPG"))


def test_undo_puts_everything_back(folder):
    before = sorted(os.listdir(folder))
    organize(folder)
    make_files(folder, "new.txt")
    organize(folder)  # a second run adds to the same log
    restored, errors = undo(folder)
    assert (restored, errors) == (5, [])
    assert sorted(os.listdir(folder)) == sorted(before + ["new.txt"])  # no category folders, no log


def test_undo_does_not_overwrite_a_new_file_with_the_same_name(folder):
    organize(folder)
    make_files(folder, "cv.pdf")
    undo(folder)
    assert os.path.exists(os.path.join(folder, "cv (1).pdf"))


def test_undo_skips_a_file_that_was_deleted(folder):
    organize(folder)
    os.remove(os.path.join(folder, "Audio", "song.mp3"))
    restored, errors = undo(folder)
    assert restored == 3
    assert len(errors) == 1


def test_undo_with_nothing_to_undo(folder):
    assert undo(folder) == (0, [])


@pytest.mark.parametrize("log", ["{ not json", json.dumps({"a": 1}), json.dumps([["a"]]), json.dumps([["../../x", "Images/x"]])])
def test_broken_log_raises_and_moves_nothing(folder, log):
    with open(os.path.join(folder, LOG_NAME), "w", encoding="utf-8") as f:
        f.write(log)
    with pytest.raises(LogError):
        organize(folder)
    with pytest.raises(LogError):
        undo(folder)
    assert os.path.exists(os.path.join(folder, "photo.JPG"))


def test_create_sample_files_never_overwrites(tmp_path):
    folder = os.path.join(tmp_path, "samples")
    assert create_sample_files(folder) == len(SAMPLE_FILES)
    with open(os.path.join(folder, "notes.txt"), "w", encoding="utf-8") as f:
        f.write("my own notes")
    assert create_sample_files(folder) == 0
    assert read(os.path.join(folder, "notes.txt")) == "my own notes"
