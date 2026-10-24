"""Session 06 project 4: a student marks analyzer (all 7 topics).

Reads a class's marks from a CSV file and answers a teacher's questions: the rank
list, each subject's average and topper, who failed, who got a distinction.
Saves everything as a text report.

Focuses on Priority 2:
- Comprehensions: list, dict and set comprehensions
- Built-ins: zip, map, enumerate, sorted, filter, any, all, sum, max
- lambda: the sort key, the filter test and the max() key
And uses Priority 1 too: a Student class, reading and writing files with exception
handling, and paths built with os.

Run it from anywhere (the files are always found next to this script):
    python Assignment/s06-python-3/project-4/marks_analyzer.py
The first run creates a sample marks.csv to work with.
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "practice_files")
DEFAULT_CSV = os.path.join(DATA_DIR, "marks.csv")
REPORT_PATH = os.path.join(DATA_DIR, "report.txt")

MAX_MARK = 100
PASS_MARK = 35
DISTINCTION_MARK = 90
GRADES = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (35, "E")]  # (lowest average, grade)
FAIL_GRADE = "F"

SAMPLE_CSV = """\
name,maths,science,english,social,computer
Asha,95,88,92,79,99
Bala,72,65,80,70,91
Chitra,45,52,38,60,55
Deepak,30,42,55,48,62
Farah,88,94,85,90,96
Gokul,64,71,33,58,70
Harini,99,97,91,94,100
Imran,55,48,62,51,67
Janani,81,79,88,84,90
Karthik,28,34,40,31,45
"""


class MarksFileError(Exception):
    """The marks file, or one line of it, can't be used."""


class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks  # subject -> mark, e.g. {"maths": 95, "science": 88}

    def total(self):
        return sum(self.marks.values())

    def average(self):
        return self.total() / len(self.marks)

    def passed(self):
        """True only if the student passed EVERY subject."""
        return all(mark >= PASS_MARK for mark in self.marks.values())

    def has_distinction(self):
        """True if the student scored a distinction in ANY subject."""
        return any(mark >= DISTINCTION_MARK for mark in self.marks.values())

    def failed_subjects(self):
        return [subject for subject, mark in self.marks.items() if mark < PASS_MARK]

    def grade(self):
        if not self.passed():
            return FAIL_GRADE
        average = self.average()
        for lowest, grade in GRADES:
            if average >= lowest:
                return grade
        return FAIL_GRADE  # not reached: passing every subject means an average of at least PASS_MARK

    def __str__(self):
        return f"{self.name}: total {self.total()}, average {self.average():.1f}, grade {self.grade()}"


def parse_header(line):
    """Return the subject names from the first line. Raises MarksFileError if it's unusable."""
    columns = [column.strip().lower() for column in line.split(",")]
    if columns[0] != "name":
        raise MarksFileError("the first line must be: name,subject1,subject2,...")
    subjects = columns[1:]
    if not subjects or not all(subjects):
        raise MarksFileError("the first line needs at least one subject, and no empty ones")
    if len(set(subjects)) != len(subjects):  # a set keeps each subject once, so a repeat makes it shorter
        raise MarksFileError("a subject appears twice in the first line")
    return subjects


def parse_row(subjects, line):
    """Turn one line of the CSV file into a Student. Raises MarksFileError for a bad line."""
    parts = [part.strip() for part in line.split(",")]
    name, values = parts[0], parts[1:]
    if not name:
        raise MarksFileError("the name is empty")
    if len(values) != len(subjects):
        raise MarksFileError(f"expected {len(subjects)} marks, got {len(values)}")
    try:
        marks = list(map(int, values))  # map() calls int() on every value
    except ValueError:
        raise MarksFileError(f"marks must be whole numbers, got {', '.join(values)}") from None
    if not all(0 <= mark <= MAX_MARK for mark in marks):
        raise MarksFileError(f"marks must be from 0 to {MAX_MARK}")
    return Student(name, dict(zip(subjects, marks)))  # zip() pairs each subject with its mark


def load_students(path):
    """Read a marks file. Returns (subjects, students, warnings about skipped lines).

    Raises FileNotFoundError if the file doesn't exist, and MarksFileError if it can't be used.
    """
    with open(path, encoding="utf-8") as f:
        # Keep each line's number for the warnings, and leave out blank lines
        lines = [(number, line) for number, line in enumerate(f, start=1) if line.strip()]
    if not lines:
        raise MarksFileError("the file is empty")

    subjects = parse_header(lines[0][1])
    students = []
    warnings = []
    seen_names = set()
    for number, line in lines[1:]:
        try:
            student = parse_row(subjects, line)
        except MarksFileError as e:
            warnings.append(f"line {number} skipped: {e}")
            continue
        if student.name.lower() in seen_names:
            warnings.append(f"line {number} skipped: {student.name} appears twice")
            continue
        seen_names.add(student.name.lower())
        students.append(student)
    return subjects, students, warnings


def create_sample_csv(path=DEFAULT_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_CSV)


def rank_list(students):
    """Highest total first. The minus sign sorts totals high to low; equal totals go in name order."""
    return sorted(students, key=lambda s: (-s.total(), s.name.lower()))


def subject_averages(subjects, students):
    return {subject: sum(s.marks[subject] for s in students) / len(students) for subject in subjects}


def subject_toppers(subjects, students):
    """subject -> the student with the highest mark in it (the first one, if there's a tie)."""
    return {subject: max(students, key=lambda s: s.marks[subject]) for subject in subjects}


def failed_students(students):
    return list(filter(lambda s: not s.passed(), students))


def distinction_students(students):
    return [s for s in students if s.has_distinction()]


def grade_counts(students):
    """Return {grade: how many students got it}, best grade first, leaving out grades nobody got."""
    grades = [s.grade() for s in students]
    order = [grade for _, grade in GRADES] + [FAIL_GRADE]
    return {grade: grades.count(grade) for grade in order if grade in grades}


def find_students(students, text):
    text = text.strip().lower()
    return [s for s in students if text in s.name.lower()]


def format_rank_list(subjects, students):
    header = f"{'Rank':<6}{'Name':<10}" + "".join(f"{subject:>9.8}" for subject in subjects) + f"{'Total':>7}{'Avg':>7} Grade"
    lines = [header]
    for rank, s in enumerate(rank_list(students), start=1):
        marks = "".join(f"{s.marks[subject]:>9}" for subject in subjects)
        lines.append(f"{rank:>4}  {s.name:<10.10}{marks}{s.total():>7}{s.average():>7.1f} {s.grade()}")
    return "\n".join(lines)


def format_subject_summary(subjects, students):
    averages = subject_averages(subjects, students)
    toppers = subject_toppers(subjects, students)
    lines = [f"{'Subject':<12}{'Average':>8}  Topper"]
    for subject in subjects:
        topper = toppers[subject]
        lines.append(f"{subject:<12}{averages[subject]:>8.1f}  {topper.name} ({topper.marks[subject]})")
    return "\n".join(lines)


def format_results(students):
    failed = failed_students(students)
    lines = [f"Failed ({len(failed)}): below {PASS_MARK} in any subject"]
    for s in failed:
        lines.append(f"  {s.name:<10} {', '.join(s.failed_subjects())}")
    if not failed:
        lines.append("  nobody")
    distinctions = distinction_students(students)
    lines.append(f"Distinction ({len(distinctions)}): {DISTINCTION_MARK} or more in any subject")
    lines.append("  " + (", ".join(s.name for s in distinctions) or "nobody"))
    return "\n".join(lines)


def format_report(subjects, students):
    passed = len(students) - len(failed_students(students))
    grades = ", ".join(f"{grade}: {count}" for grade, count in grade_counts(students).items())
    return "\n\n".join([
        "CLASS REPORT",
        format_rank_list(subjects, students),
        format_subject_summary(subjects, students),
        format_results(students),
        f"Grades: {grades}\nPass rate: {passed}/{len(students)} ({passed / len(students):.0%})",
    ]) + "\n"


def save_report(text, path=REPORT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def load(path):
    """Load a marks file, explaining what went wrong instead of crashing.
    Returns (subjects, students), or None if the file can't be used."""
    try:
        subjects, students, warnings = load_students(path)
    except FileNotFoundError:
        print(f"  No such file: {os.path.abspath(path)}")
    except IsADirectoryError:
        print(f"  That's a folder, not a file: {os.path.abspath(path)}")
    except UnicodeDecodeError:
        print("  That's not a text file.")
    except (MarksFileError, OSError) as e:
        print(f"  Can't use {path}: {e}")
    else:
        for warning in warnings:
            print("  warning:", warning)
        if not students:
            print("  The file has no valid students.")
            return None
        print(f"Loaded {len(students)} students and {len(subjects)} subjects.")
        return subjects, students
    return None


MENU = """
1. Rank list                  5. Save the full report
2. Subject summary            6. Load another CSV file
3. Failed and distinctions    7. Quit
4. Find a student"""


def main():
    if not os.path.exists(DEFAULT_CSV):
        create_sample_csv()
        print(f"Created a sample marks file: {DEFAULT_CSV}")
    data = load(DEFAULT_CSV)
    if data is None:
        print(f"Fix or delete {DEFAULT_CSV} and run again.")
        return
    subjects, students = data

    while True:
        print(MENU)
        choice = input("Choose 1-7: ").strip()

        if choice == "1":
            print(format_rank_list(subjects, students))

        elif choice == "2":
            print(format_subject_summary(subjects, students))

        elif choice == "3":
            print(format_results(students))

        elif choice == "4":
            found = find_students(students, input("Name (or part of it): "))
            for s in found:
                print(" ", s)
                if s.failed_subjects():
                    print("    failed:", ", ".join(s.failed_subjects()))
            if not found:
                print("  No student found.")

        elif choice == "5":
            try:
                save_report(format_report(subjects, students))
            except OSError as e:
                print("  Could not save the report:", e)
            else:
                print(f"  Saved the report to {REPORT_PATH}")

        elif choice == "6":
            data = load(input("Path to a CSV file: ").strip())
            if data is not None:  # keep the old data if the new file can't be used
                subjects, students = data

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl + C or Ctrl + D
        print("\nGoodbye!")
