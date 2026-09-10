"""Verify cloud connection settings without contacting a real database."""

import os
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from database import Database


class DatabaseConfigurationTests(TestCase):
    """Protect URL precedence and SSL behavior during local/cloud switching."""

    def test_cloud_url_preserves_ssl_and_ignores_local_host(self):
        """Neon URLs must reach libpq unchanged, including their SSL options."""
        url = "postgresql://example:example@cloud.invalid/db?sslmode=require&channel_binding=require"
        with patch.dict(os.environ, {"DATABASE_URL": url, "db_host": "wrong.local"}, clear=True):
            with patch("database.psycopg2.connect") as connect:
                db = Database()
                connect.assert_called_once_with(url, connect_timeout=15)
                db.close()
                connect.return_value.close.assert_called_once()

    def test_local_fallback_and_explicit_ssl(self):
        """Empty URL uses local settings, with an optional explicit SSL mode."""
        with patch.dict(os.environ, {"DATABASE_URL": "", "db_host": "localhost", "DB_SSLMODE": "require"}, clear=True):
            with patch("database.psycopg2.connect") as connect:
                Database().close()
                self.assertEqual(connect.call_args.kwargs["host"], "localhost")
                self.assertEqual(connect.call_args.kwargs["sslmode"], "require")
