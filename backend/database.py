import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Database:
    """Manage the PostgreSQL connection and query/transaction lifecycle for an operation."""

    def __init__(self):
        """Open a connection from environment variables; do not log password information."""
        self.conn = psycopg2.connect(
            connect_timeout=5,
            host=os.getenv("db_host", "localhost"),
            port=os.getenv("db_port", "5432"),
            database=os.getenv("db_name", "course_registration_system"),
            user=os.getenv("db_user", "postgres"),
            password=os.getenv("db_password", ""),
        )

    def execute_query(self, query, params=None):
        """Execute a write and commit; return the affected row count instead of a closed cursor."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount

        except Exception:
            self.conn.rollback()
            raise

        finally:
            cursor.close()

    def execute(self, query, params=None):
        """Execute a write in the current transaction; the caller commits explicitly."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.rowcount
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """Read one row as a dictionary or None and always close the cursor after the query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchone()

        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Read all rows as dictionaries; keep the transaction and locks for the caller."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()

        finally:
            cursor.close()

    def close(self):
        """Close the connection; PostgreSQL rolls back uncommitted transactions and releases locks."""
        if self.conn:
            self.conn.close()


def get_db():
    """Create a dedicated connection for the operation; the caller must close it in a finally block."""
    return Database()
