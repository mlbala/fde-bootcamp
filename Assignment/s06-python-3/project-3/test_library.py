import ast
import json
import os

import pytest

from library import (
    MAX_BOOKS_PER_MEMBER,
    Book,
    BookNotFoundError,
    BookUnavailableError,
    InvalidBookError,
    Library,
    LibraryError,
    book_from_dict,
)

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.py")

# Topics 1-4 only: nothing from topics 5-7 (comprehensions, built-ins, lambda)
FORBIDDEN = {"ListComp", "DictComp", "SetComp", "GeneratorExp", "Lambda",
             "any()", "all()", "map()", "filter()", "enumerate()", "zip()", "sorted()"}


def constructs_used(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    used = set()
    for node in ast.walk(tree):
        used.add(type(node).__name__)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used.add(node.func.id + "()")
    return used


@pytest.fixture
def library(tmp_path):
    lib = Library(path=os.path.join(tmp_path, "data", "library.json"))
    lib.add_sample_books()
    return lib


def titles(books):
    names = []
    for book in books:
        names.append(book.title)
    return names


def test_uses_only_topics_1_to_4():
    assert constructs_used(SCRIPT) & FORBIDDEN == set()


def test_book_cleans_its_fields():
    book = Book(1, "  Clean Code ", " Robert C. Martin ", "2008")
    assert (book.title, book.author, book.year) == ("Clean Code", "Robert C. Martin", 2008)
    assert book.is_available()


@pytest.mark.parametrize(
    "title, author, year",
    [("", "A", 2000), ("   ", "A", 2000), ("T", "", 2000), ("T", None, 2000), ("T", "A", "abc"), ("T", "A", 1200), ("T", "A", 9999)],
)
def test_invalid_book_raises(title, author, year):
    with pytest.raises(InvalidBookError):
        Book(1, title, author, year)


def test_every_custom_error_is_a_library_error():
    for error in (InvalidBookError, BookNotFoundError, BookUnavailableError):
        assert issubclass(error, LibraryError)


def test_ids_count_up_and_are_never_reused(library):
    assert list(library.books) == [1, 2, 3, 4, 5, 6]
    library.remove_book(6)
    assert library.add_book("New Book", "Someone", 2020).id == 7


def test_duplicate_book_is_refused(library):
    with pytest.raises(InvalidBookError, match=r"already in the library \(#3\)"):
        library.add_book("clean code", "ROBERT C. MARTIN", 2008)


def test_get_unknown_id(library):
    with pytest.raises(BookNotFoundError):
        library.get(42)


def test_borrow_and_return(library):
    book = library.borrow(5, " Bala ")
    assert book.borrower == "Bala"
    assert not book.is_available()
    library.return_book(5)
    assert book.is_available()


def test_cannot_borrow_a_borrowed_book(library):
    library.borrow(5, "Bala")
    with pytest.raises(BookUnavailableError, match="already borrowed by Bala"):
        library.borrow(5, "Kumar")


def test_member_limit(library):
    for book_id in range(1, MAX_BOOKS_PER_MEMBER + 1):
        library.borrow(book_id, "Bala")
    with pytest.raises(LibraryError, match="already has"):
        library.borrow(6, "bala")  # names are compared ignoring case


def test_borrow_needs_a_member_name(library):
    with pytest.raises(LibraryError):
        library.borrow(1, "   ")


def test_return_a_book_that_is_not_borrowed(library):
    with pytest.raises(BookUnavailableError):
        library.return_book(1)


def test_remove(library):
    library.remove_book(1)
    assert 1 not in library.books
    library.borrow(2, "Bala")
    with pytest.raises(BookUnavailableError):
        library.remove_book(2)


def test_search_matches_title_or_author_ignoring_case(library):
    assert titles(library.search("PYTHON")) == [
        "Python Crash Course",
        "Automate the Boring Stuff with Python",
        "Fluent Python",
        "Think Python",
    ]
    assert titles(library.search("martin")) == ["Clean Code"]
    assert library.search("no such book") == []


def test_available_leaves_out_borrowed_books(library):
    library.borrow(1, "Bala")
    assert 1 not in [b.id for b in library.available()]
    assert len(library.available()) == 5


def test_stats(library):
    assert library.stats()["borrowed"] == 0
    library.borrow(1, "Bala")
    library.borrow(6, "Bala")
    library.borrow(3, "Kumar")
    stats = library.stats()
    assert (stats["total"], stats["borrowed"], stats["available"]) == (6, 3, 3)
    assert stats["oldest"].title == "Clean Code"
    assert stats["loans"] == {"Bala": ["Python Crash Course", "Think Python"], "Kumar": ["Clean Code"]}


def test_save_and_load_round_trip(library):
    library.borrow(2, "Bala")
    library.save()  # also creates the missing "data" folder
    loaded = Library(path=library.path)
    assert loaded.load() == []
    assert [b.to_dict() for b in loaded.books.values()] == [b.to_dict() for b in library.books.values()]
    assert loaded.next_id == 7  # carries on after the highest id in the file


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        Library(path=os.path.join(tmp_path, "nothing.json")).load()


def test_load_broken_json_sets_the_file_aside(tmp_path):
    path = os.path.join(tmp_path, "library.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write("{ this is not json")
    lib = Library(path=path)
    warnings = lib.load()
    assert len(warnings) == 1
    assert "not valid JSON" in warnings[0]
    assert lib.books == {}
    assert not os.path.exists(path)
    assert os.path.exists(path + ".broken")


def test_load_skips_bad_records(tmp_path):
    path = os.path.join(tmp_path, "library.json")
    records = [
        {"id": 1, "title": "Good", "author": "A", "year": 2000, "borrower": None},
        {"id": 2, "title": "", "author": "A", "year": 2000},
        {"id": 3, "author": "A", "year": 2000},
        "not a dict",
        {"id": 1, "title": "Same id", "author": "B", "year": 2001},
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f)
    lib = Library(path=path)
    warnings = lib.load()
    assert list(lib.books) == [1]
    assert len(warnings) == 4


def test_book_from_dict_treats_empty_borrower_as_on_the_shelf():
    book = book_from_dict({"id": "4", "title": "T", "author": "A", "year": 2000, "borrower": ""})
    assert book.id == 4
    assert book.is_available()
