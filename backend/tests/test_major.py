"""Major mutation API regressions without accessing a real database."""
import unittest
from unittest.mock import MagicMock, patch

import jwt
from flask import Flask
from config import JWT_SECRET, JWT_ALGORITHM
from routes.user_routes import admin_bp


class MajorMutationTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(admin_bp)
        self.client = app.test_client()
        token = jwt.encode(
            {"user_id": "admin_test", "role": "admin"},
            JWT_SECRET, algorithm=JWT_ALGORITHM,
        )
        self.headers = {"Authorization": f"Bearer {token}"}

    def request_major(self, method, affected):
        auth_db = MagicMock()
        auth_db.fetch_one.return_value = {"active_status": True}
        db = MagicMock()
        db.execute_query.return_value = affected
        with patch("utils.auth.get_db", return_value=auth_db), patch(
            "models.admin.get_db", return_value=db
        ):
            response = self.client.open(
                "/api/admin/majors/TEST", method=method,
                json={"major_name": "Updated name"} if method == "PUT" else None,
                headers=self.headers,
            )
        db.close.assert_called_once()
        db.execute_query.assert_called_once()
        self.assertEqual(db.execute_query.call_args.args[1],
                         ("Updated name", "TEST") if method == "PUT" else ("TEST",))
        return response

    def test_missing_major_update_returns_404(self):
        response = self.request_major("PUT", 0)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Major not found"})

    def test_missing_major_delete_returns_404(self):
        response = self.request_major("DELETE", 0)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Major not found"})

    def test_existing_major_update_succeeds(self):
        response = self.request_major("PUT", 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Major updated successfully"})

    def test_existing_major_delete_succeeds(self):
        response = self.request_major("DELETE", 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Major deleted successfully"})
