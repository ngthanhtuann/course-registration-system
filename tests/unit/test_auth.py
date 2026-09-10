"""Import-level unit check for the authentication service boundary."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from services.auth_service import User


class AuthTests(unittest.TestCase):
    """Verify the service exposes the account model."""

    def test_user_starts_without_identity(self):
        """Anonymous construction is used by the login route."""
        self.assertEqual(User().identity, {})
