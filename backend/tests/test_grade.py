"""Keep grade precision and pass/fail results consistent with numeric(4,2)."""
from decimal import Decimal
import unittest
from unittest.mock import MagicMock, patch

from models.grade import GradeRecord
from models.lecturer import Lecturer


class GradeConsistencyTests(unittest.TestCase):
    def test_result_uses_the_grade_that_will_be_stored(self):
        for raw, stored, result in [
            (4.994, 4.99, "not passed"),
            (4.995, 5.0, "passed"),
            (4.999, 5.0, "passed"),
            (0, 0, "not passed"),
            (5, 5, "passed"),
            (10, 10, "passed"),
            (Decimal("4.995"), 5, "passed"),
        ]:
            with self.subTest(raw=raw):
                record = GradeRecord(raw)
                self.assertEqual(record.calculateResultStatus(), result)
                self.assertEqual(record.grade, stored)

    def test_missing_grade_has_no_result(self):
        self.assertIsNone(GradeRecord().calculateResultStatus())

    def test_invalid_grades_are_rejected_before_rounding(self):
        for value in [-0.001, 10.001, float("nan"), float("inf")]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                GradeRecord(value).calculateResultStatus()

    def test_save_returns_same_grade_and_result_as_database_write(self):
        db = MagicMock()
        db.fetch_one.return_value = {"semester_id": "S1"}
        db.fetch_all.return_value = [{"ended": True}]
        with patch("models.lecturer.get_db", return_value=db):
            response = Lecturer({"user_id": "L1"}).manageStudentGrade("R1", {"grade": 4.995})
        self.assertEqual(db.execute_query.call_args.args[1], (5.0, "passed", "R1"))
        self.assertEqual(response["grade"], 5.0)
        self.assertEqual(response["result_status"], "passed")
        db.close.assert_called_once()
