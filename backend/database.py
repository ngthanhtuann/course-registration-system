import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Database:
    """Connect to PostgreSQL and run database queries."""

    def __init__(self):
        """Open a PostgreSQL connection using values from .env."""
        url = os.getenv("DATABASE_URL", "").strip()
        kwargs = {"connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "15"))}
        sslmode = os.getenv("DB_SSLMODE", "").strip()
        if sslmode:
            kwargs["sslmode"] = sslmode
        if url:
            self.conn = psycopg2.connect(url, **kwargs)
        else:
            self.conn = psycopg2.connect(
                host=os.getenv("db_host", "localhost"),
                port=os.getenv("db_port", "5432"),
                database=os.getenv("db_name", "course_registration_system"),
                user=os.getenv("db_user", "postgres"),
                password=os.getenv("db_password", ""),
                **kwargs,
            )
        # Use the project timezone for SQL date/time operations.
        with self.conn.cursor() as cursor:
            cursor.execute("select set_config('TimeZone', %s, true)",
                           (os.getenv("DB_TIMEZONE", "Asia/Ho_Chi_Minh"),))

    def execute_query(self, query, params=None):
        """Run an INSERT, UPDATE or DELETE query and save the change."""
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
        """Run a write query without committing yet."""
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
        """Return one row from a SELECT query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchone()

        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Return all rows from a SELECT query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()

        finally:
            cursor.close()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


def get_db():
    """Create and return a database connection."""
    return Database()
