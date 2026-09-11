"""Validation tests for login and profile updates; no real database is used."""

import unittest
from unittest.mock import MagicMock, patch

from models.user import User


class UserValidationTests(unittest.TestCase):
    def test_login_rejects_non_string_username_or_password(self):
        invalid_payloads = [
            {"username": None, "password": "Password123"},
            {"username": 123, "password": "Password123"},
            {"username": {}, "password": "Password123"},
            {"username": [], "password": "Password123"},
            {"username": "student01", "password": None},
            {"username": "student01", "password": 123},
        ]

        with patch("models.user.get_db") as get_db:
            for payload in invalid_payloads:
                with self.subTest(payload=payload):
                    result = User().login(payload)
                    self.assertEqual(result, ({"error": "invalid username or password input"}, 400))
            get_db.assert_not_called()

    def test_login_rejects_missing_or_blank_credentials(self):
        payloads = [
            {},
            {"username": "", "password": "Password123"},
            {"username": "   ", "password": "Password123"},
            {"username": "student01", "password": ""},
        ]

        with patch("models.user.get_db") as get_db:
            for payload in payloads:
                with self.subTest(payload=payload):
                    result = User().login(payload)
                    self.assertEqual(result, ({"error": "username and password are required"}, 400))
            get_db.assert_not_called()

    def test_update_profile_rejects_invalid_email_without_database_write(self):
        invalid_emails = ["invalid", "abc@", "@gmail.com", "abc gmail.com"]
        identity = {"user_id": "STU001", "username": "student01", "role": "student"}

        with patch("models.user.get_db") as get_db:
            for email in invalid_emails:
                with self.subTest(email=email):
                    result = User(identity).updateProfile({"fullname": "Student One", "email": email})
                    self.assertEqual(result, ({"error": "Invalid email format"}, 400))
            get_db.assert_not_called()

    def test_update_profile_accepts_valid_email_and_updates_database(self):
        identity = {"user_id": "STU001", "username": "student01", "role": "student"}
        db = MagicMock()
        db.fetch_one.return_value = None

        with patch("models.user.get_db", return_value=db):
            result = User(identity).updateProfile(
                {"fullname": "Student One", "email": "student@uth.edu.vn"}
            )

        self.assertEqual(result, {"message": "profile updated successfully"})
        db.execute.assert_called_once()
        db.conn.commit.assert_called_once()
        db.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
