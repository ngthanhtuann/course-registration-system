"""Pure unit checks for registration-related models."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from models.grade import GradeRecord


class RegistrationTests(unittest.TestCase):
    """Verify grade status calculation independently of PostgreSQL."""

    def test_passing_grade_has_passing_status(self):
        """A grade at least five must be marked passed."""
        grade = GradeRecord(8)
        self.assertEqual(grade.calculateResultStatus(), "passed")
