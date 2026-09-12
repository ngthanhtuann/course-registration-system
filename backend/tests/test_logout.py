"""Exercise real login/JWT/logout with mocked account storage."""
import secrets
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
from routes.auth_routes import auth_bp
from utils.auth import revoked_tokens, is_token_revoked
from utils.password import hash_password


class LogoutTests(unittest.TestCase):
    def setUp(self):
        revoked_tokens.clear()
        self.addCleanup(revoked_tokens.clear)
        app = Flask(__name__)
        app.register_blueprint(auth_bp)
        self.client = app.test_client()

    def test_logout_revokes_only_old_token_and_relogin_works(self):
        password = secrets.token_urlsafe(16)
        db = MagicMock()
        db.fetch_one.return_value = {
            "user_id": "A1", "username": "admin", "role": "admin",
            "full_name": "Admin", "email": "admin@example.invalid",
            "active_status": True, "password_hash": hash_password(password),
        }
        with patch("models.user.get_db", return_value=db), patch(
            "utils.auth.get_db", return_value=db
        ):
            def login():
                response = self.client.post("/api/login", json={
                    "username": "admin", "password": password,
                })
                self.assertEqual(response.status_code, 200)
                return response.json["token"]

            token = login()
            headers = {"Authorization": f"Bearer {token}"}
            self.assertEqual(self.client.get("/api/me", headers=headers).status_code, 200)
            self.assertEqual(self.client.post("/api/logout", headers=headers).status_code, 200)
            self.assertEqual(self.client.get("/api/me", headers=headers).status_code, 401)
            new_token = login()
            self.assertNotEqual(token, new_token)
            self.assertEqual(self.client.get("/api/me", headers={
                "Authorization": f"Bearer {new_token}",
            }).status_code, 200)
            self.assertEqual(self.client.get("/api/me", headers=headers).status_code, 401)

    def test_expired_denylist_entries_are_removed(self):
        revoked_tokens.update({"expired": 10, "valid": 30})
        with patch("utils.auth.time", return_value=20):
            self.assertFalse(is_token_revoked("expired"))
            self.assertTrue(is_token_revoked("valid"))
        self.assertNotIn("expired", revoked_tokens)
