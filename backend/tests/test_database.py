"""Pool regression tests; no network or real database credentials required."""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Event
import unittest
from unittest.mock import MagicMock, patch

import psycopg2
from psycopg2.extensions import TRANSACTION_STATUS_IDLE
from psycopg2.extras import RealDictCursor, RealDictRow

import database


class DatabasePoolTests(unittest.TestCase):
    def setUp(self):
        self.connections = []
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {
            "DATABASE_URL": "", "DB_POOL_MIN": "1", "DB_POOL_MAX": "2",
            "DB_CONNECT_TIMEOUT": "1", "DB_SSLMODE": "",
            "DB_TIMEZONE": "Asia/Ho_Chi_Minh",
            "db_host": "localhost", "db_port": "5432", "db_name": "test",
            "db_user": "test", "db_password": "",
        }, clear=True).start()
        patch.object(database, "_pool_state", None).start()
        patch.object(database.atexit, "register").start()
        self.connect = patch.object(psycopg2, "connect", side_effect=self.new_connection).start()

    def new_connection(self, *args, **kwargs):
        conn = MagicMock()
        conn.closed = False
        conn.info.transaction_status = TRANSACTION_STATUS_IDLE
        conn.close.side_effect = lambda: setattr(conn, "closed", True)
        cursor = conn.cursor.return_value
        cursor.__enter__.return_value = cursor
        cursor.rowcount = 1
        cursor.fetchone.return_value = RealDictRow(value=1)
        cursor.fetchall.return_value = [RealDictRow(value=1)]
        self.connections.append(conn)
        return conn

    def test_reuse_and_idempotent_close(self):
        first = database.get_db()
        conn = first.conn
        first.close()
        first.close()
        second = database.get_db()
        self.assertIs(second.conn, conn)
        self.assertEqual(self.connect.call_count, 1)
        conn.close.assert_not_called()
        second.close()

    def test_url_and_ssl_options(self):
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://localhost/test", "DB_SSLMODE": "require"}):
            db = database.get_db()
        self.connect.assert_called_once_with("postgresql://localhost/test", connect_timeout=1, sslmode="require")
        db.close()

    def test_fallback_configuration(self):
        db = database.get_db()
        self.connect.assert_called_once_with(connect_timeout=1, host="localhost", port="5432",
                                             database="test", user="test", password="")
        db.close()

    def test_transaction_and_return_types(self):
        db = database.get_db()
        conn = db.conn
        conn.cursor.return_value.execute.assert_called_with(
            "select set_config('TimeZone', %s, true)", ("Asia/Ho_Chi_Minh",))
        self.assertEqual(db.execute("write"), 1)
        conn.commit.assert_not_called()
        self.assertIsInstance(db.fetch_one("read"), RealDictRow)
        self.assertIsInstance(db.fetch_all("read")[0], RealDictRow)
        conn.cursor.assert_called_with(cursor_factory=RealDictCursor)
        conn.commit.assert_not_called()
        db.conn.commit()
        self.assertEqual(db.execute_query("write"), 1)
        self.assertEqual(conn.commit.call_count, 2)
        db.close()
        conn.rollback.assert_called_once()

    def test_all_query_errors_rollback_and_preserve_exception(self):
        for method in ("execute", "execute_query", "fetch_one", "fetch_all"):
            with self.subTest(method=method):
                db = database.get_db()
                conn = db.conn
                conn.rollback.reset_mock()
                error = psycopg2.ProgrammingError("invalid query")
                conn.cursor.return_value.execute.side_effect = error
                with self.assertRaises(psycopg2.ProgrammingError) as raised:
                    getattr(db, method)("invalid")
                self.assertIs(raised.exception, error)
                conn.rollback.assert_called_once()
                conn.cursor.return_value.execute.side_effect = None
                db.close()

    def test_failed_rollback_discards_connection(self):
        db = database.get_db()
        conn = db.conn
        conn.rollback.side_effect = psycopg2.OperationalError("lost connection")
        db.close()
        self.assertTrue(conn.closed)
        replacement = database.get_db()
        self.assertIsNot(replacement.conn, conn)
        replacement.close()

    def test_failed_timezone_setup_returns_connection(self):
        original = self.new_connection

        def fail_setup(*args, **kwargs):
            conn = original()
            conn.cursor.return_value.execute.side_effect = psycopg2.OperationalError("setup failed")
            return conn

        self.connect.side_effect = fail_setup
        with self.assertRaises(psycopg2.OperationalError):
            database.get_db()
        self.assertEqual(len(database._pool_state[0]._used), 0)
        self.connections[0].cursor.return_value.execute.side_effect = None
        database.get_db().close()

    def test_failed_getconn_releases_slot(self):
        database.get_db().close()
        pool = database._pool_state[0]
        with patch.object(pool, "getconn", side_effect=psycopg2.OperationalError("offline")):
            with self.assertRaises(psycopg2.OperationalError):
                database.get_db()
        first, second = database.get_db(), database.get_db()
        first.close()
        second.close()

    def test_concurrent_requests_have_separate_connections(self):
        barrier = Barrier(2)

        def request():
            db = database.get_db()
            try:
                barrier.wait(timeout=5)
                return id(db.conn)
            finally:
                db.close()

        with ThreadPoolExecutor(max_workers=2) as executor:
            ids = list(executor.map(lambda _: request(), range(2)))
        self.assertEqual(len(set(ids)), 2)
        self.assertEqual(self.connect.call_count, 2)
        self.assertEqual(len(database._pool_state[0]._used), 0)

    def test_full_pool_waits_then_reuses_connection(self):
        with patch.dict(os.environ, {"DB_POOL_MAX": "1"}):
            first = database.get_db()
        started = Event()

        def request():
            started.set()
            second = database.get_db()
            second.close()

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(request)
            self.assertTrue(started.wait(timeout=5))
            self.assertFalse(future.done())
            first.close()
            future.result(timeout=5)
        self.assertEqual(self.connect.call_count, 1)

    def test_pool_timeout_is_operational_error(self):
        with patch.dict(os.environ, {"DB_POOL_MAX": "1"}):
            db = database.get_db()
        try:
            with self.assertRaises(psycopg2.OperationalError):
                database.get_db()
        finally:
            db.close()
        database.get_db().close()

    def test_invalid_pool_limits(self):
        for minimum, maximum in (("0", "5"), ("3", "2")):
            with patch.dict(os.environ, {"DB_POOL_MIN": minimum, "DB_POOL_MAX": maximum}):
                with self.assertRaises(ValueError):
                    database.get_db()
        self.connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()
