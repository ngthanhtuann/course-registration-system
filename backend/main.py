import os
from time import perf_counter

import psycopg2

from flask import (
    Flask,
    g,
    jsonify,
    request,
)

from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from database import (
    close_request_db,
    get_connection_pool,
    get_db,
)

from routes.auth_routes import auth_bp
from routes.user_routes import admin_bp
from routes.student_routes import student_bp
from routes.teaching_routes import lecturer_bp

from utils.http_support import ISOJSONProvider


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

app.json = ISOJSONProvider(app)


# ============================================================
# CORS
# ============================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": os.getenv(
                "CORS_ORIGINS",
                (
                    "http://localhost:8443,"
                    "http://127.0.0.1:8443"
                ),
            ).split(",")
        }
    },
)


# ============================================================
# REGISTER ROUTES
# ============================================================

app.register_blueprint(
    auth_bp
)

app.register_blueprint(
    admin_bp
)

app.register_blueprint(
    student_bp
)

app.register_blueprint(
    lecturer_bp
)


# ============================================================
# REQUEST TIMER
# ============================================================

@app.before_request
def start_request_timer():
    """
    Save the start time of the HTTP request.
    """

    g.request_start_time = perf_counter()


@app.after_request
def log_request_time(response):
    """
    Print total backend request time.
    """

    start = getattr(
        g,
        "request_start_time",
        None
    )

    if start is not None:

        elapsed = (
            perf_counter()
            - start
        )

        print(
            f"[REQUEST] "
            f"{request.method} "
            f"{request.path} "
            f"status={response.status_code} "
            f"time={elapsed:.3f}s"
        )

    return response


# ============================================================
# RELEASE DATABASE CONNECTION
# ============================================================

@app.teardown_request
def release_request_database(
    error=None
):
    """
    Return the request-scoped PostgreSQL connection
    to the shared pool.
    """

    close_request_db(error)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return jsonify(
        {
            "message":
            "course registration system backend is running"
        }
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    try:

        db = get_db()

        version = db.fetch_one(
            """
            select max(version) as version
            from schema_version
            """
        )

        if (
            not version
            or version["version"] != 1
        ):

            return jsonify(
                {
                    "status": "error",
                    "database": "unavailable"
                }
            ), 503

        return jsonify(
            {
                "status": "ok",
                "database": "ok"
            }
        )

    except Exception:

        return jsonify(
            {
                "status": "error",
                "database": "unavailable"
            }
        ), 503


# ============================================================
# HTTP ERROR HANDLER
# ============================================================

@app.errorhandler(HTTPException)
def http_error(error):

    response = error.get_response()

    response.set_data(
        app.json.dumps(
            {
                "error":
                error.description
            }
        )
    )

    response.content_type = (
        "application/json"
    )

    return response


# ============================================================
# DATABASE UNAVAILABLE
# ============================================================

@app.errorhandler(
    psycopg2.OperationalError
)
@app.errorhandler(
    psycopg2.InterfaceError
)
def database_unavailable(error):

    return jsonify(
        {
            "error":
            "database temporarily unavailable"
        }
    ), 503


# ============================================================
# DATABASE CONSTRAINT ERROR
# ============================================================

@app.errorhandler(
    psycopg2.IntegrityError
)
def invalid_database_write(error):

    return jsonify(
        {
            "error":
            (
                "data conflicts with existing "
                "records or database constraints"
            )
        }
    ), 409


# ============================================================
# INVALID DATABASE VALUE
# ============================================================

@app.errorhandler(
    psycopg2.DataError
)
def invalid_database_value(error):

    return jsonify(
        {
            "error":
            "invalid data format"
        }
    ), 400


# ============================================================
# UNEXPECTED SERVER ERROR
# ============================================================

@app.errorhandler(Exception)
def unexpected_server_error(error):

    app.logger.exception(
        "Unhandled server error"
    )

    return jsonify(
        {
            "error":
            "internal server error"
        }
    ), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    # Open DB_POOL_MIN physical connections before
    # browser requests start arriving.
    #
    # Startup may take a few seconds because Neon is remote,
    # but page requests can immediately reuse warm connections.

    try:

        get_connection_pool()

        print(
            "[DB POOL] ready"
        )

    except psycopg2.Error as exc:

        print(
            "[DB POOL] warm-up failed: "
            f"{type(exc).__name__}"
        )

    app.run(

        host=os.getenv(
            "HOST",
            "127.0.0.1"
        ),

        port=int(
            os.getenv(
                "PORT",
                "5000"
            )
        ),

        debug=os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower() == "true",
    )