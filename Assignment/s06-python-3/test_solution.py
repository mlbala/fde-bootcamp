import os

import pytest

from solution import Expense, ExpenseTracker, InvalidExpenseError, parse_line


@pytest.fixture
def tracker(tmp_path):
    t = ExpenseTracker(path=os.path.join(tmp_path, "expenses.csv"))
    t.add("Lunch", "250", "Food")
    t.add("Metro card", 500, "transport")
    t.add("Dinner", 400.5, " food ")
    return t


def test_expense_cleans_its_fields():
    e = Expense("  Coffee ", "80", " Food ")
    assert e.description == "Coffee"
    assert e.amount == 80.0
    assert e.category == "food"


@pytest.mark.parametrize("amount", ["abc", "", "-5", "0", 0, -10])
def test_invalid_amount_raises(amount):
    with pytest.raises(InvalidExpenseError):
        Expense("Lunch", amount, "food")


@pytest.mark.parametrize(
    "description, category",
    [("", "food"), ("   ", "food"), ("Lunch", ""), ("Lunch, coffee", "food"), ("Lunch", "fo,od")],
)
def test_invalid_text_fields_raise(description, category):
    with pytest.raises(InvalidExpenseError):
        Expense(description, "100", category)


def test_parse_line_round_trip():
    original = Expense("Lunch", "250", "food")
    parsed = parse_line(original.to_line() + "\n")
    assert (parsed.description, parsed.amount, parsed.category) == ("Lunch", 250.0, "food")


def test_parse_line_wrong_number_of_fields():
    with pytest.raises(InvalidExpenseError):
        parse_line("Lunch,250\n")


def test_total(tracker):
    assert tracker.total() == pytest.approx(1150.5)


def test_total_by_category(tracker):
    assert tracker.total_by_category() == {"food": pytest.approx(650.5), "transport": 500.0}


def test_in_category_ignores_case_and_spaces(tracker):
    assert [e.description for e in tracker.in_category(" FOOD ")] == ["Lunch", "Dinner"]


def test_largest(tracker):
    assert [e.description for e in tracker.largest(2)] == ["Metro card", "Dinner"]


def test_add_invalid_does_not_change_tracker(tracker):
    with pytest.raises(InvalidExpenseError):
        tracker.add("Snacks", "free", "food")
    assert len(tracker.expenses) == 3


def test_save_and_load_round_trip(tracker):
    tracker.save()
    loaded = ExpenseTracker(path=tracker.path)
    assert loaded.load() == 0
    assert [e.to_line() for e in loaded.expenses] == [e.to_line() for e in tracker.expenses]


def test_save_creates_missing_folder(tmp_path):
    path = os.path.join(tmp_path, "new", "folder", "expenses.csv")
    t = ExpenseTracker(path=path)
    t.add("Lunch", "250", "food")
    t.save()
    assert os.path.isfile(path)


def test_load_missing_file_starts_empty(tmp_path):
    t = ExpenseTracker(path=os.path.join(tmp_path, "does_not_exist.csv"))
    assert t.load() == 0
    assert t.expenses == []


def test_load_skips_bad_lines(tmp_path):
    path = os.path.join(tmp_path, "expenses.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write("description,amount,category\n")
        f.write("Lunch,250,food\n")
        f.write("Broken line\n")
        f.write("Taxi,abc,transport\n")
        f.write("\n")
        f.write("Movie,300,fun\n")
    t = ExpenseTracker(path=path)
    assert t.load() == 2
    assert [e.description for e in t.expenses] == ["Lunch", "Movie"]
