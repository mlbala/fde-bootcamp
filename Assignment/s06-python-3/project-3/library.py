"""Session 06 project 3: a library management system (topics 1-4: exceptions, os, files, OOP).

The first project with real classes. Uses topics 1-4 of the session, on top of sessions 04-05:
- OOP: a Book class and a Library class, with attributes, methods, __str__ and self.
  The library keeps its own state: the books, the file it saves to, and the next id
- Exception handling: a family of custom exceptions under one LibraryError base class,
  raise for bad input, try / except / else in the menu
- File handling: the library is saved as JSON after every change and loaded at start-up
- os: the file path is built from __file__, and a broken file is moved out of the way

It doesn't use comprehensions, lambda or the session's built-ins yet (topics 5-7,
project 4), so searching, filtering and counting are done with plain for loops.

Run it from anywhere (the data file is always found next to this script):
    python Assignment/s06-python-3/project-3/library.py
"""

import json
import os
from datetime import date

# Build the path from this file's location, not the cwd (see 02_os_and_paths.ipynb)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(SCRIPT_DIR, "practice_files", "library.json")
MAX_BOOKS_PER_MEMBER = 3
FIRST_YEAR = 1450  # around when the printing press was invented

SAMPLE_BOOKS = [
    ("Python Crash Course", "Eric Matthes", 2019),
    ("Automate the Boring Stuff with Python", "Al Sweigart", 2019),
    ("Clean Code", "Robert C. Martin", 2008),
    ("The Pragmatic Programmer", "David Thomas", 2019),
    ("Fluent Python", "Luciano Ramalho", 2022),
    ("Think Python", "Allen B. Downey", 2015),
]


class LibraryError(Exception):
    """Base class for every library error, so the menu can catch them all with one except."""


class InvalidBookError(LibraryError):
    """A book's title, author or year is not valid."""


class BookNotFoundError(LibraryError):
    """No book has the given id."""


class BookUnavailableError(LibraryError):
    """The book can't be borrowed (it's already out), returned or removed (it is out)."""


def clean_text(value, field):
    """Return value without surrounding spaces. Raises InvalidBookError if it's empty or not text."""
    if not isinstance(value, str) or not value.strip():
        raise InvalidBookError(f"{field} cannot be empty")
    return value.strip()


class Book:
    def __init__(self, book_id, title, author, year, borrower=None):
        title = clean_text(title, "title")
        author = clean_text(author, "author")
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise InvalidBookError(f"year must be a whole number, got '{year}'")
        this_year = date.today().year
        if not FIRST_YEAR <= year <= this_year:
            raise InvalidBookError(f"year must be from {FIRST_YEAR} to {this_year}, got {year}")

        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.borrower = borrower or None  # "" in the file means "on the shelf" too

    def is_available(self):
        return self.borrower is None

    def is_same_book(self, other):
        """True if other has the same title and author, ignoring case."""
        return self.title.lower() == other.title.lower() and self.author.lower() == other.author.lower()

    def to_dict(self):
        """Return this book as a dict, ready for json.dump()."""
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year, "borrower": self.borrower}

    def __str__(self):
        status = "on the shelf" if self.is_available() else f"borrowed by {self.borrower}"
        return f"#{self.id:<4}{self.title:<40.40}{self.author:<20.20}{self.year:<6}{status}"


def book_from_dict(record):
    """Build a Book from one record of the JSON file. Raises InvalidBookError for a bad record."""
    try:
        return Book(int(record["id"]), record["title"], record["author"], record["year"], record.get("borrower"))
    except KeyError as e:
        raise InvalidBookError(f"missing field {e}")
    except (TypeError, ValueError, AttributeError):  # the record isn't a dict, or the id isn't a number
        raise InvalidBookError(f"not a valid book record: {record!r}")


class Library:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.books = {}  # id -> Book, so finding a book by id is one lookup
        self.next_id = 1  # ids are never reused, even after a book is removed

    def add_book(self, title, author, year):
        """Validate and add a book. Raises InvalidBookError if it's invalid or already here."""
        book = Book(self.next_id, title, author, year)
        for existing in self.books.values():
            if existing.is_same_book(book):
                raise InvalidBookError(f"'{book.title}' by {book.author} is already in the library (#{existing.id})")
        self.books[book.id] = book
        self.next_id += 1
        return book

    def add_sample_books(self):
        for title, author, year in SAMPLE_BOOKS:
            self.add_book(title, author, year)

    def get(self, book_id):
        """Return the book with this id. Raises BookNotFoundError if there isn't one."""
        try:
            return self.books[book_id]
        except KeyError:
            # Turn the low-level KeyError into an error that explains the problem.
            # "from None" hides the KeyError, so the traceback only shows ours.
            raise BookNotFoundError(f"no book with id {book_id}") from None

    def borrowed_by(self, member):
        """Return the books this member has, ignoring case in the name."""
        member = member.strip().lower()
        books = []
        for book in self.books.values():
            if book.borrower is not None and book.borrower.lower() == member:
                books.append(book)
        return books

    def borrow(self, book_id, member):
        """Lend a book to a member. Raises a LibraryError if that isn't possible."""
        member = member.strip()
        if not member:
            raise LibraryError("member name cannot be empty")
        book = self.get(book_id)
        if not book.is_available():
            raise BookUnavailableError(f"'{book.title}' is already borrowed by {book.borrower}")
        if len(self.borrowed_by(member)) >= MAX_BOOKS_PER_MEMBER:
            raise LibraryError(f"{member} already has {MAX_BOOKS_PER_MEMBER} books, return one first")
        book.borrower = member
        return book

    def return_book(self, book_id):
        book = self.get(book_id)
        if book.is_available():
            raise BookUnavailableError(f"'{book.title}' is not borrowed")
        book.borrower = None
        return book

    def remove_book(self, book_id):
        book = self.get(book_id)
        if not book.is_available():
            raise BookUnavailableError(f"'{book.title}' is borrowed by {book.borrower}, it can't be removed")
        del self.books[book_id]
        return book

    def search(self, text):
        """Return the books whose title or author contains text, ignoring case."""
        text = text.strip().lower()
        found = []
        for book in self.books.values():
            if text in book.title.lower() or text in book.author.lower():
                found.append(book)
        return found

    def available(self):
        books = []
        for book in self.books.values():
            if book.is_available():
                books.append(book)
        return books

    def stats(self):
        borrowed = 0
        oldest = None
        loans = {}  # member -> titles they have
        for book in self.books.values():
            if oldest is None or book.year < oldest.year:
                oldest = book
            if not book.is_available():
                borrowed += 1
                if book.borrower not in loans:
                    loans[book.borrower] = []
                loans[book.borrower].append(book.title)
        return {
            "total": len(self.books),
            "borrowed": borrowed,
            "available": len(self.books) - borrowed,
            "oldest": oldest,
            "loans": loans,
        }

    def save(self):
        """Write every book to the JSON file, creating its folder if needed."""
        records = []
        for book in self.books.values():
            records.append(book.to_dict())
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def load(self):
        """Replace the books with those saved in the file.

        Raises FileNotFoundError if nothing has been saved yet: the caller decides what
        a first run should do. Returns a list of warnings about anything that was skipped.
        """
        try:
            with open(self.path, encoding="utf-8") as f:
                records = json.load(f)
        except ValueError as e:  # json.JSONDecodeError and UnicodeDecodeError are both ValueErrors
            return [self._set_aside(f"not valid JSON ({e})")]
        if not isinstance(records, list):
            return [self._set_aside("not a list of books")]

        self.books = {}
        self.next_id = 1
        warnings = []
        number = 0
        for record in records:
            number += 1
            try:
                book = book_from_dict(record)
            except InvalidBookError as e:
                warnings.append(f"skipped book {number} in the file: {e}")
                continue
            if book.id in self.books:
                warnings.append(f"skipped book {number} in the file: id {book.id} is used twice")
                continue
            self.books[book.id] = book
            if book.id >= self.next_id:
                self.next_id = book.id + 1
        return warnings

    def _set_aside(self, reason):
        """Rename a broken data file, so the next save doesn't overwrite it, and start empty."""
        broken_path = self.path + ".broken"
        os.replace(self.path, broken_path)  # unlike os.rename, replaces an old .broken file on Windows too
        self.books = {}
        self.next_id = 1
        return f"{os.path.basename(self.path)} is {reason}; renamed it to {os.path.basename(broken_path)}"


def print_books(books):
    if not books:
        print("  No books found.")
        return
    for book in books:
        print(" ", book)


def ask_id():
    """Keep asking until the user types a whole number."""
    while True:
        text = input("Book id: ").strip().lstrip("#")
        try:
            return int(text)
        except ValueError:
            print("  The id is a whole number, e.g. 3")


def save(library, message):
    """Save after a change. A failed save is reported, but the program keeps running."""
    try:
        library.save()
    except OSError as e:
        print(f"  {message}. Could not save: {e}")
    else:
        print(f"  {message}. Saved.")


MENU = """
1. List books           5. Return a book
2. Search               6. Remove a book
3. Add a book           7. Statistics
4. Borrow a book        8. Quit"""


def main():
    library = Library()
    try:
        warnings = library.load()
    except FileNotFoundError:
        library.add_sample_books()
        save(library, f"First run: starting with {len(library.books)} sample books")
    else:
        print(f"Loaded {len(library.books)} books from {library.path}")
        for warning in warnings:
            print("warning:", warning)

    while True:
        print(MENU)
        choice = input("Choose 1-8: ").strip()
        try:
            if choice == "1":
                if input("Only books on the shelf? (y/n): ").strip().lower() == "y":
                    print_books(library.available())
                else:
                    print_books(list(library.books.values()))

            elif choice == "2":
                print_books(library.search(input("Search title or author: ")))

            elif choice == "3":
                book = library.add_book(input("Title: "), input("Author: "), input("Year: "))
                save(library, f"Added #{book.id} '{book.title}'")

            elif choice == "4":
                book = library.borrow(ask_id(), input("Member name: "))
                save(library, f"'{book.title}' borrowed by {book.borrower}")

            elif choice == "5":
                book = library.return_book(ask_id())
                save(library, f"'{book.title}' is back on the shelf")

            elif choice == "6":
                book = library.remove_book(ask_id())
                save(library, f"Removed '{book.title}'")

            elif choice == "7":
                stats = library.stats()
                print(f"  Books: {stats['total']}   on the shelf: {stats['available']}   borrowed: {stats['borrowed']}")
                if stats["oldest"] is not None:
                    print(f"  Oldest: {stats['oldest'].title} ({stats['oldest'].year})")
                if stats["borrowed"] == 0:
                    print("  Every book is on the shelf.")
                for member, titles in stats["loans"].items():
                    print(f"  {member:<15}{', '.join(titles)}")

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Please enter a number from 1 to 8.")

        except LibraryError as e:  # catches InvalidBookError, BookNotFoundError and BookUnavailableError too
            print("  Error:", e)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl + C or Ctrl + D
        print("\nGoodbye! (every change was already saved)")
