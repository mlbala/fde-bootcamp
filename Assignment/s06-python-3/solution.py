"""Session 06 mini project: an expense tracker.

Brings the session's topics together:
- OOP: an Expense class and an ExpenseTracker class
- Exception handling: validating with raise, a custom exception, try/except/else
- File handling: saving to and loading from a CSV-style text file
- os: building the file path from this script's own folder
- Comprehensions and built-ins: totals, filtering and sorting

Run it from anywhere (the data file is always found next to this script):
    python Assignment/s06-python-3/solution.py
"""

import os

# Build the path from this file's location, not the cwd (see 02_os_and_paths.ipynb)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(SCRIPT_DIR, "practice_files", "expenses.csv")
HEADER = "description,amount,category"


class InvalidExpenseError(Exception):
    """Raised when an expense has a bad description, amount or category."""


class Expense:
    def __init__(self, description, amount, category):
        description = description.strip()
        category = category.strip().lower()

        if not description:
            raise InvalidExpenseError("description cannot be empty")
        if not category:
            raise InvalidExpenseError("category cannot be empty")
        if "," in description or "," in category:
            raise InvalidExpenseError("commas are not allowed (the file uses them as separators)")

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise InvalidExpenseError(f"amount must be a number, got '{amount}'")
        if amount <= 0:
            raise InvalidExpenseError(f"amount must be positive, got {amount}")

        self.description = description
        self.amount = amount
        self.category = category

    def to_line(self):
        """Return this expense as one line of the CSV file."""
        return f"{self.description},{self.amount},{self.category}"

    def __str__(self):
        return f"{self.description:<20}{self.amount:>10.2f}  [{self.category}]"


def parse_line(line):
    """Turn one CSV line into an Expense. Raises InvalidExpenseError for a bad line."""
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidExpenseError(f"expected 3 comma-separated values, got {len(parts)}")
    description, amount, category = parts
    return Expense(description, amount, category)


class ExpenseTracker:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.expenses = []

    def add(self, description, amount, category):
        """Validate and add an expense. Raises InvalidExpenseError if it's invalid."""
        expense = Expense(description, amount, category)
        self.expenses.append(expense)
        return expense

    def total(self):
        return sum(e.amount for e in self.expenses)

    def total_by_category(self):
        """Return {category: total}, sorted by category name."""
        categories = sorted({e.category for e in self.expenses})
        return {c: sum(e.amount for e in self.expenses if e.category == c) for c in categories}

    def in_category(self, category):
        category = category.strip().lower()
        return [e for e in self.expenses if e.category == category]

    def largest(self, n=3):
        return sorted(self.expenses, key=lambda e: e.amount, reverse=True)[:n]

    def save(self):
        """Write every expense to the file, creating its folder if needed."""
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n")
            for expense in self.expenses:
                f.write(expense.to_line() + "\n")

    def load(self):
        """Replace the expenses with those in the file.

        A missing file is normal on the first run, so it just means "no expenses yet".
        Bad lines are skipped with a warning. Returns the number of lines skipped.
        """
        self.expenses = []
        skipped = 0
        try:
            with open(self.path, encoding="utf-8") as f:
                for line_number, line in enumerate(f, start=1):
                    if not line.strip() or line.strip() == HEADER:
                        continue
                    try:
                        self.expenses.append(parse_line(line))
                    except InvalidExpenseError as e:
                        print(f"warning: skipping line {line_number}: {e}")
                        skipped += 1
        except FileNotFoundError:
            pass
        return skipped


MENU = """
1. Add an expense
2. List all expenses
3. Summary by category
4. Top 3 expenses
5. Save and quit"""


def print_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    for number, expense in enumerate(expenses, start=1):
        print(f"{number:>2}. {expense}")


def main():
    tracker = ExpenseTracker()
    skipped = tracker.load()
    print(f"Loaded {len(tracker.expenses)} expenses from {tracker.path}")
    if skipped:
        print(f"Skipped {skipped} invalid lines")

    while True:
        print(MENU)
        choice = input("Choose 1-5: ").strip()

        if choice == "1":
            description = input("Description: ")
            amount = input("Amount: ")
            category = input("Category: ")
            try:
                expense = tracker.add(description, amount, category)
            except InvalidExpenseError as e:
                print("Not added:", e)
            else:
                print("Added:", expense)

        elif choice == "2":
            print_expenses(tracker.expenses)

        elif choice == "3":
            for category, amount in tracker.total_by_category().items():
                print(f"{category:<15}{amount:>10.2f}")
            print(f"{'TOTAL':<15}{tracker.total():>10.2f}")

        elif choice == "4":
            print_expenses(tracker.largest(3))

        elif choice == "5":
            try:
                tracker.save()
            except OSError as e:
                print("Could not save:", e)   # stay in the menu so nothing is lost
            else:
                print(f"Saved {len(tracker.expenses)} expenses to {tracker.path}")
                break

        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):   # Ctrl + C or Ctrl + D
        print("\nExiting without saving.")
