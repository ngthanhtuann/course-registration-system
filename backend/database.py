import atexit
import os
import threading
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


_pool_state = None
_pool_lock = threading.Lock()


def _get_pool():
    """Lazily create one pool per backend process, including CLI entry points."""
    global _pool_state
    with _pool_lock:
        if _pool_state is not None:
            return _pool_state
        minimum = int(os.getenv("DB_POOL_MIN", "1"))
        maximum = int(os.getenv("DB_POOL_MAX", "5"))
        if not 1 <= minimum <= maximum:
            raise ValueError("DB_POOL_MIN and DB_POOL_MAX must satisfy 1 <= min <= max")
        url = os.getenv("DATABASE_URL", "").strip()
        kwargs = {"connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "15"))}
        sslmode = os.getenv("DB_SSLMODE", "").strip()
        if sslmode:
            kwargs["sslmode"] = sslmode
        if not url:
            kwargs.update(
                host=os.getenv("db_host", "localhost"),
                port=os.getenv("db_port", "5432"),
                database=os.getenv("db_name", "course_registration_system"),
                user=os.getenv("db_user", "postgres"),
                password=os.getenv("db_password", ""),
            )
        pool = ThreadedConnectionPool(minimum, maximum, *([url] if url else []), **kwargs)
        # ThreadedConnectionPool itself raises immediately when full. Bound the
        # number of borrowers and allow concurrent requests to wait for a slot.
        _pool_state = (pool, threading.BoundedSemaphore(maximum),
                       max(1, kwargs["connect_timeout"]))
        atexit.register(pool.closeall)
        return _pool_state


class Database:
    """Borrow a PostgreSQL connection and run database queries."""

    def __init__(self):
        """Keep one exclusive connection until close(), preserving transactions."""
        self.conn = None
        self._pool, self._slots, timeout = _get_pool()
        if not self._slots.acquire(timeout=timeout):
            raise psycopg2.OperationalError("Timed out waiting for a database connection")
        try:
            self.conn = self._pool.getconn()
        except BaseException:
            self._slots.release()
            raise
        # Use the project timezone for SQL date/time operations.
        # Keep the existing transaction-local scope for Neon transaction pooling.
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("select set_config('TimeZone', %s, true)",
                               (os.getenv("DB_TIMEZONE", "Asia/Ho_Chi_Minh"),))
        except BaseException:
            self.close()
            raise

    def _rollback_after_error(self):
        """Preserve the query exception and discard a connection that cannot reset."""
        try:
            self.conn.rollback()
        except Exception:
            self.conn.close()

    def execute_query(self, query, params=None):
        """Run an INSERT, UPDATE or DELETE query and save the change."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount

        except Exception:
            self._rollback_after_error()
            raise

        finally:
            cursor.close()

    def execute(self, query, params=None):
        """Run a write query without committing yet."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.rowcount
        except Exception:
            self._rollback_after_error()
            raise
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """Return one row from a SELECT query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchone()

        except Exception:
            self._rollback_after_error()
            raise

        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Return all rows from a SELECT query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()

        except Exception:
            self._rollback_after_error()
            raise

        finally:
            cursor.close()

    def close(self):
        """Rollback unfinished work and return the connection exactly once."""
        conn, self.conn = self.conn, None
        if conn is None:
            return
        discard = bool(conn.closed)
        try:
            if not discard:
                try:
                    conn.rollback()
                except Exception:
                    discard = True
            self._pool.putconn(conn, close=discard)
        finally:
            self._slots.release()


def get_db():
    """Create a database handle borrowing from the shared connection pool."""
    return Database()
