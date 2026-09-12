import os
from threading import Lock
from time import perf_counter

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool, PoolError
from dotenv import load_dotenv
from flask import g, has_request_context


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)


# ============================================================
# SHARED CONNECTION POOL
# ============================================================

_connection_pool = None
_pool_lock = Lock()


def get_connection_pool():
    """
    Create one shared PostgreSQL connection pool.

    DB_POOL_MIN:
        Number of connections opened and kept ready.

    DB_POOL_MAX:
        Maximum number of connections Flask can borrow.
    """

    global _connection_pool

    with _pool_lock:

        if _connection_pool is not None:
            return _connection_pool

        url = os.getenv(
            "DATABASE_URL",
            ""
        ).strip()

        timezone = os.getenv(
            "DB_TIMEZONE",
            "Asia/Ho_Chi_Minh"
        ).strip()

        min_connections = int(
            os.getenv(
                "DB_POOL_MIN",
                "4"
            )
        )

        max_connections = int(
            os.getenv(
                "DB_POOL_MAX",
                "10"
            )
        )

        if min_connections < 1:
            min_connections = 1

        if max_connections < min_connections:
            max_connections = min_connections

        kwargs = {
            "connect_timeout": int(
                os.getenv(
                    "DB_CONNECT_TIMEOUT",
                    "15"
                )
            ),

            # Set timezone once when the physical connection
            # is created.
            #
            # Do NOT execute SELECT set_config(...) every time
            # a request borrows the connection.
            "options": f"-c timezone={timezone}",
        }

        sslmode = os.getenv(
            "DB_SSLMODE",
            ""
        ).strip()

        if sslmode:
            kwargs["sslmode"] = sslmode

        # ====================================================
        # NEON / DATABASE_URL
        # ====================================================

        if url:

            _connection_pool = ThreadedConnectionPool(
                min_connections,
                max_connections,
                url,
                **kwargs,
            )

        # ====================================================
        # LOCAL POSTGRESQL FALLBACK
        # ====================================================

        else:

            _connection_pool = ThreadedConnectionPool(
                min_connections,
                max_connections,

                host=os.getenv(
                    "db_host",
                    "localhost"
                ),

                port=os.getenv(
                    "db_port",
                    "5432"
                ),

                database=os.getenv(
                    "db_name",
                    "course_registration_system"
                ),

                user=os.getenv(
                    "db_user",
                    "postgres"
                ),

                password=os.getenv(
                    "db_password",
                    ""
                ),

                **kwargs,
            )

        return _connection_pool


# ============================================================
# DATABASE CLASS
# ============================================================

class Database:
    """
    Database helper.

    During one Flask HTTP request, the same Database object
    and PostgreSQL connection are reused.

    Outside Flask requests, for example:
        setup_database.py
        create_admin.py

    the connection is released immediately by close().
    """

    def __init__(self, request_scoped=False):

        self.pool = get_connection_pool()

        self.conn = None

        self.request_scoped = request_scoped

        try:

            start = perf_counter()

            self.conn = self.pool.getconn()

            elapsed = perf_counter() - start

            print(
                f"[DB CONNECTION] "
                f"getconn = {elapsed:.3f}s"
            )

        except PoolError as exc:

            raise psycopg2.OperationalError(
                "database is busy"
            ) from exc

        if (
            self.conn is None
            or self.conn.closed
        ):

            if self.conn is not None:
                self.pool.putconn(
                    self.conn,
                    close=True
                )

            self.conn = None

            raise psycopg2.OperationalError(
                "database connection is unavailable"
            )


    # ========================================================
    # INSERT / UPDATE / DELETE + COMMIT
    # ========================================================

    def execute_query(
        self,
        query,
        params=None
    ):
        """
        Execute an INSERT, UPDATE or DELETE query
        and commit immediately.
        """

        cursor = self.conn.cursor(
            cursor_factory=RealDictCursor
        )

        try:

            start = perf_counter()

            cursor.execute(
                query,
                params
            )

            self.conn.commit()

            elapsed = perf_counter() - start

            print(
                f"[DB QUERY] "
                f"execute_query = {elapsed:.3f}s"
            )

            return cursor.rowcount

        except Exception:

            self.conn.rollback()

            raise

        finally:

            cursor.close()


    # ========================================================
    # WRITE WITHOUT COMMIT
    # ========================================================

    def execute(
        self,
        query,
        params=None
    ):
        """
        Execute a query without committing.

        Useful when multiple statements must belong to
        the same transaction.
        """

        cursor = self.conn.cursor(
            cursor_factory=RealDictCursor
        )

        try:

            start = perf_counter()

            cursor.execute(
                query,
                params
            )

            elapsed = perf_counter() - start

            print(
                f"[DB QUERY] "
                f"execute = {elapsed:.3f}s"
            )

            return cursor.rowcount

        except Exception:

            self.conn.rollback()

            raise

        finally:

            cursor.close()


    # ========================================================
    # FETCH ONE
    # ========================================================

    def fetch_one(
        self,
        query,
        params=None
    ):
        """Return one row."""

        cursor = self.conn.cursor(
            cursor_factory=RealDictCursor
        )

        try:

            start = perf_counter()

            cursor.execute(
                query,
                params
            )

            result = cursor.fetchone()

            elapsed = perf_counter() - start

            print(
                f"[DB QUERY] "
                f"fetch_one = {elapsed:.3f}s"
            )

            return result

        finally:

            cursor.close()


    # ========================================================
    # FETCH ALL
    # ========================================================

    def fetch_all(
        self,
        query,
        params=None
    ):
        """Return all matching rows."""

        cursor = self.conn.cursor(
            cursor_factory=RealDictCursor
        )

        try:

            start = perf_counter()

            cursor.execute(
                query,
                params
            )

            result = cursor.fetchall()

            elapsed = perf_counter() - start

            print(
                f"[DB QUERY] "
                f"fetch_all = {elapsed:.3f}s"
            )

            return result

        finally:

            cursor.close()


    # ========================================================
    # RELEASE CONNECTION
    # ========================================================

    def _release(self):
        """
        Return the physical PostgreSQL connection
        to the pool.
        """

        if self.conn is None:
            return

        conn = self.conn

        self.conn = None

        try:

            if not conn.closed:

                # SELECT also opens a transaction in psycopg2.
                #
                # Rollback unfinished transaction before
                # returning the connection to the pool.
                conn.rollback()

            self.pool.putconn(conn)

        except (
            psycopg2.OperationalError,
            psycopg2.InterfaceError,
        ):

            self.pool.putconn(
                conn,
                close=True
            )


    def close(self):
        """
        Outside Flask request:
            release immediately.

        Inside Flask request:
            do nothing here.

        main.py teardown_request will release it once
        at the end of the HTTP request.
        """

        if (
            self.request_scoped
            and has_request_context()
        ):
            return

        self._release()


# ============================================================
# GET DATABASE
# ============================================================

def get_db():
    """
    Return one Database object per Flask HTTP request.

    This means:

        require_auth()
              ↓
        business logic
              ↓
        model queries

    all reuse the SAME PostgreSQL connection.
    """

    if has_request_context():

        db = g.get(
            "_database"
        )

        if db is None:

            db = Database(
                request_scoped=True
            )

            g._database = db

        return db

    # Scripts such as:
    #
    # setup_database.py
    # create_admin.py

    return Database(
        request_scoped=False
    )


# ============================================================
# END OF REQUEST
# ============================================================

def close_request_db(
    error=None
):
    """
    Return the request-scoped connection
    to the pool exactly once.
    """

    if not has_request_context():
        return

    db = g.pop(
        "_database",
        None
    )

    if db is not None:
        db._release()
