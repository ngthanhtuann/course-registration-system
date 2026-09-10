"""Pure unit checks for the Course model."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from models.course import Course


class CourseTests(unittest.TestCase):
    """Verify course value validation without database access."""

    def test_positive_integer_rejects_non_positive_values(self):
        """Capacity and credit values must be positive integers."""
        self.assertTrue(Course.positiveInteger(1))
        with self.assertRaises(ValueError):
            Course.positiveInteger(0)
        self.assertEqual(Course.positiveInteger("1"), 1)
