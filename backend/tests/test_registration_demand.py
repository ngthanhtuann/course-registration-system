"""Run model SELECTs over inline fixtures; no real DB, tables or data changes."""
import sqlite3
import unittest
from unittest.mock import MagicMock, patch

from models.admin import Administrator


FIXTURES = """
with courses(course_code, course_name) as (values ('X', 'Shared'), ('Y', 'Empty')),
curriculum(course_code, major_code) as (values ('X', 'A'), ('X', 'B'), ('Y', 'A')),
students(student_id, user_id, major_code) as (
    values ('A1', 'U1', 'A'), ('A2', 'U2', 'A'), ('B1', 'U3', 'B')),
users(user_id, full_name, email) as (
    values ('U1', 'One', 'one@example.invalid'), ('U2', 'Two', 'two@example.invalid'),
           ('U3', 'Three', 'three@example.invalid')),
registrations(registration_id, student_id, course_code, period_id, registration_status) as (
    values ('R1', 'A1', 'X', 'P1', 'registered'),
           ('R2', 'A2', 'X', 'P1', 'registered'),
           ('R3', 'B1', 'X', 'P1', 'registered'),
           ('R4', 'A1', 'X', 'P2', 'registered'),
           ('R5', 'A2', 'X', 'P1', 'dropped'))
"""


class RegistrationDemandTests(unittest.TestCase):
    def test_counts_and_details_filter_student_major(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.row_factory = sqlite3.Row
        db = MagicMock()
        # SQLite supports these SELECT/FILTER expressions; adapt only placeholders.
        db.fetch_all.side_effect = lambda sql, args: [dict(row) for row in
            connection.execute(FIXTURES + sql.replace("%s", "?"), args)]
        with patch("models.admin.get_db", return_value=db):
            for major, ids in [("A", ["A1", "A2"]), ("B", ["B1"]),
                               (None, ["A1", "A2", "B1"])]:
                with self.subTest(major=major):
                    query = {"period_id": "P1", "major_code": major}
                    report = Administrator().generateRegistrationDemandReport(query)
                    self.assertEqual(report[0]["registered_students"], len(ids))
                    details = Administrator().demand_students("X", query)
                    self.assertEqual([row["student_id"] for row in details], ids)
                    if major != "B":
                        self.assertEqual(report[1]["registered_students"], 0)
        self.assertEqual(db.close.call_count, 6)
