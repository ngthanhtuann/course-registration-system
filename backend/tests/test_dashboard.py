"""Dashboard response contract; no real database is used."""
from datetime import date
import unittest
from unittest.mock import MagicMock, patch

from models.admin import Administrator


class DashboardTests(unittest.TestCase):
    def test_one_query_preserves_counts_and_semester_dates(self):
        db = MagicMock()
        db.fetch_one.return_value = {
            "total_students": 10, "active_lecturers": 2,
            "total_courses": 5, "active_registrations": 7,
            "semester_id": "S1", "semester_name": "Semester 1",
            "start_date": date(2026, 1, 1), "end_date": date(2026, 12, 31),
        }
        with patch("models.admin.get_db", return_value=db):
            result = Administrator().dashboard()
        self.assertEqual(result, {
            "total_students": 10, "active_lecturers": 2,
            "total_courses": 5, "active_registrations": 7,
            "active_semester": {"semester_id": "S1", "semester_name": "Semester 1",
                                "start_date": date(2026, 1, 1), "end_date": date(2026, 12, 31)},
        })
        db.fetch_one.assert_called_once()
        db.close.assert_called_once()

    def test_no_current_semester_stays_null(self):
        db = MagicMock()
        db.fetch_one.return_value = {
            "total_students": 0, "active_lecturers": 0,
            "total_courses": 0, "active_registrations": 0,
            "semester_id": None, "semester_name": None,
            "start_date": None, "end_date": None,
        }
        with patch("models.admin.get_db", return_value=db):
            self.assertIsNone(Administrator().dashboard()["active_semester"])
        db.close.assert_called_once()
