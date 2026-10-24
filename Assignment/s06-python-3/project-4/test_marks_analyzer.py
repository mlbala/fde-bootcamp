import os

import pytest

from marks_analyzer import (
    MarksFileError,
    Student,
    create_sample_csv,
    distinction_students,
    failed_students,
    find_students,
    format_rank_list,
    format_report,
    grade_counts,
    load_students,
    parse_header,
    parse_row,
    rank_list,
    save_report,
    subject_averages,
    subject_toppers,
)

SUBJECTS = ["maths", "science"]


@pytest.fixture
def students():
    return [
        Student("Asha", {"maths": 95, "science": 80}),  # total 175, distinction
        Student("Bala", {"maths": 30, "science": 70}),  # total 100, failed maths
        Student("Chitra", {"maths": 85, "science": 90}),  # total 175, distinction
        Student("Deepak", {"maths": 60, "science": 55}),  # total 115, average 57.5 (grade D)
    ]


def write(tmp_path, text):
    path = os.path.join(tmp_path, "marks.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def test_student_methods():
    s = Student("Asha", {"maths": 95, "science": 80})
    assert (s.total(), s.average(), s.passed(), s.has_distinction()) == (175, 87.5, True, True)
    assert s.grade() == "A"


def test_one_failed_subject_means_fail_whatever_the_average():
    s = Student("Gokul", {"maths": 100, "science": 100, "english": 34})
    assert not s.passed()
    assert s.failed_subjects() == ["english"]
    assert s.grade() == "F"


@pytest.mark.parametrize("average, grade", [(95, "A+"), (90, "A+"), (89, "A"), (70, "B"), (60, "C"), (50, "D"), (35, "E")])
def test_grade_boundaries(average, grade):
    assert Student("X", {"maths": average}).grade() == grade


def test_parse_header():
    assert parse_header(" Name , Maths ,science\n") == ["maths", "science"]


@pytest.mark.parametrize("line", ["student,maths\n", "name\n", "name,maths,,science\n", "name,maths,Maths\n"])
def test_bad_header(line):
    with pytest.raises(MarksFileError):
        parse_header(line)


def test_parse_row_pairs_subjects_with_marks():
    s = parse_row(SUBJECTS, " Asha , 95, 80\n")
    assert (s.name, s.marks) == ("Asha", {"maths": 95, "science": 80})


@pytest.mark.parametrize("line", [",95,80", "Asha,95", "Asha,95,80,70", "Asha,95,eighty", "Asha,95.5,80", "Asha,101,80", "Asha,-1,80"])
def test_bad_row(line):
    with pytest.raises(MarksFileError):
        parse_row(SUBJECTS, line)


def test_load_skips_bad_lines_and_blank_lines(tmp_path):
    path = write(tmp_path, "name,maths,science\nAsha,95,80\n\nBala,abc,70\nasha,50,50\nChitra,85,90\n")
    subjects, students, warnings = load_students(path)
    assert subjects == SUBJECTS
    assert [s.name for s in students] == ["Asha", "Chitra"]
    assert len(warnings) == 2
    assert warnings[0].startswith("line 4")  # line numbers count the blank line
    assert "appears twice" in warnings[1]


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_students(os.path.join(tmp_path, "nope.csv"))


def test_load_empty_file(tmp_path):
    with pytest.raises(MarksFileError, match="empty"):
        load_students(write(tmp_path, "\n\n"))


def test_sample_file_loads_without_warnings(tmp_path):
    path = os.path.join(tmp_path, "data", "marks.csv")
    create_sample_csv(path)
    subjects, students, warnings = load_students(path)
    assert (len(subjects), len(students), warnings) == (5, 10, [])


def test_rank_list_breaks_ties_by_name(students):
    assert [s.name for s in rank_list(students)] == ["Asha", "Chitra", "Deepak", "Bala"]


def test_subject_averages(students):
    assert subject_averages(SUBJECTS, students) == {"maths": 67.5, "science": 73.75}


def test_subject_toppers(students):
    toppers = subject_toppers(SUBJECTS, students)
    assert (toppers["maths"].name, toppers["science"].name) == ("Asha", "Chitra")


def test_failed_and_distinction(students):
    assert [s.name for s in failed_students(students)] == ["Bala"]
    assert [s.name for s in distinction_students(students)] == ["Asha", "Chitra"]


def test_grade_counts_best_first(students):
    assert grade_counts(students) == {"A": 2, "D": 1, "F": 1}


def test_find_students_ignores_case_and_matches_part_of_the_name(students):
    assert [s.name for s in find_students(students, " a ")] == ["Asha", "Bala", "Chitra", "Deepak"]
    assert [s.name for s in find_students(students, "CHI")] == ["Chitra"]
    assert find_students(students, "zz") == []


def test_rank_list_table(students):
    lines = format_rank_list(SUBJECTS, students).splitlines()
    assert lines[1].split() == ["1", "Asha", "95", "80", "175", "87.5", "A"]
    assert len(lines) == 5


def test_report_is_saved(students, tmp_path):
    report = format_report(SUBJECTS, students)
    assert "Pass rate: 3/4 (75%)" in report
    assert "Bala       maths" in report
    path = os.path.join(tmp_path, "out", "report.txt")
    save_report(report, path)
    with open(path, encoding="utf-8") as f:
        assert f.read() == report
