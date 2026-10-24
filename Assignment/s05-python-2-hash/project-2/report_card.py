"""Session 05 project 2: a report card generator (topics 1-2: hash and string formatting).

Uses topics 1 and 2 of the session, on top of the basics from sessions 04-05:
- String formatting: a str.format() template with named fields filled from a dict with **,
  alignment, width, a width taken from a variable, fill characters, precision,
  percentages, dates, and f-strings
- Hash: dicts as lookup tables (the grade from the average, PASS/FAIL from True/False),
  and a SHA-256 verification code that changes if any detail on the card is edited

There's no if / else, no loops and no functions of your own yet: that's topic 3
(projects 3-5). So the five subjects are written out one by one. Notice how
repetitive that is: it's exactly the problem loops and functions solve.
Type whole numbers from 0 to 100 for the marks: checking the input needs if (topic 3).

Run it with:
    python Assignment/s05-python-2-hash/project-2/report_card.py
"""

import hashlib
from datetime import date

SCHOOL = "FDE PUBLIC SCHOOL"
WIDTH = 52
PASS_MARK = 40
OUT_OF = 100
SUBJECTS = 5

# The grade comes from the "tens" of the average: 87.5 -> 8 -> "A". A dict lookup instead of if / elif.
GRADES = {10: "A+", 9: "A+", 8: "A", 7: "B", 6: "C", 5: "D", 4: "E", 3: "F", 2: "F", 1: "F", 0: "F"}
RESULT = {True: "PASS", False: "FAIL"}

# A template with named fields; {width} inside another field's spec sets its width from a variable
HEADER = """\
{double_line}
{school:^{width}}
{title:^{width}}
{double_line}
Name : {name:<24}Roll no: {roll:>12}
Date : {date:%d %B %Y}
{line}"""
ROW = "{:<20}{:>10}{:>10}{:>12}"  # 20 + 10 + 10 + 12 = WIDTH

print("Enter the student's details.")
name = input("Name: ").strip().title()  # " asha " -> "Asha"
roll = input("Roll number: ").strip().upper()
maths = int(input("Maths: "))
science = int(input("Science: "))
english = int(input("English: "))
social = int(input("Social: "))
computer = int(input("Computer: "))

total = maths + science + english + social + computer
max_total = SUBJECTS * OUT_OF
average = total / SUBJECTS
passed_all = min(maths, science, english, social, computer) >= PASS_MARK  # failing one subject fails the year

tens = max(0, min(10, int(average // 10)))  # keep it a key of GRADES, even for a mistyped mark
grade = {True: GRADES[tens], False: "F"}[passed_all]

# Hash every detail on the card. Change one mark and the code is completely different,
# so anyone can recompute it to check that the card wasn't edited.
details = "{}|{}|{}|{}|{}|{}|{}".format(name, roll, maths, science, english, social, computer)
digest = hashlib.sha256(details.encode()).hexdigest()[:12].upper()
code = "{}-{}-{}".format(digest[:4], digest[4:8], digest[8:])

card = {
    "double_line": "=" * WIDTH,
    "line": "-" * WIDTH,
    "width": WIDTH,
    "school": SCHOOL,
    "title": "REPORT CARD - {:%Y}".format(date.today()),
    "name": name,
    "roll": roll,
    "date": date.today(),
}

print()
print(HEADER.format(**card))  # ** fills each {field} from the dict entry with the same name
print(ROW.format("Subject", "Marks", "Out of", "Result"))
print(ROW.format("Maths", maths, OUT_OF, RESULT[maths >= PASS_MARK]))
print(ROW.format("Science", science, OUT_OF, RESULT[science >= PASS_MARK]))
print(ROW.format("English", english, OUT_OF, RESULT[english >= PASS_MARK]))
print(ROW.format("Social", social, OUT_OF, RESULT[social >= PASS_MARK]))
print(ROW.format("Computer", computer, OUT_OF, RESULT[computer >= PASS_MARK]))
print("-" * WIDTH)
print(f"{'Total':<20}{total:>10}{max_total:>10}")
print(f"{'Average':<20}{average:>10.2f}")
print(f"{'Percentage':<20}{total / max_total:>10.1%}")  # % multiplies by 100 and adds the sign
print(f"{'Grade':<20}{grade:>10}")
print(f"{'Result':<20}{RESULT[passed_all]:>10}")
print("=" * WIDTH)
print(f"Verification code: {code}")
print(f"{'(pass mark ' + str(PASS_MARK) + ' in every subject)':>{WIDTH}}")
