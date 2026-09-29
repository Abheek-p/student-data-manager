import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import student_result_management as app


class StudentResultTests(unittest.TestCase):
    def test_pass_grade(self):
        marks = {subject: 80 for subject in app.SUBJECTS}
        total, percentage, grade = app.calculate_result(marks)
        self.assertEqual(total, 400)
        self.assertEqual(percentage, 80)
        self.assertEqual(grade, "A")

    def test_fail_when_subject_below_35(self):
        marks = {subject: 80 for subject in app.SUBJECTS}
        marks["Physics"] = 20
        _, _, grade = app.calculate_result(marks)
        self.assertEqual(grade, "FAIL")

    def test_find_student(self):
        students = [{"roll_no": "101", "name": "Test"}]
        self.assertEqual(app.find_student(students, "101")["name"], "Test")


if __name__ == "__main__":
    unittest.main()
