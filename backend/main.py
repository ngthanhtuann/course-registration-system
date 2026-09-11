import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.user_routes import admin_bp
from routes.student_routes import student_bp
from routes.teaching_routes import lecturer_bp

from utils.http_support import ISOJSONProvider

app = Flask(__name__)
app.json = ISOJSONProvider(app)
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "http://localhost:8443,http://127.0.0.1:8443").split(",")}})

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(lecturer_bp)


@app.get("/")
def home():
    """Show that the backend is running."""
    return jsonify({"message": "course registration system backend is running"})


@app.get("/api/health")
def health():
    """Check whether the backend can connect to the database."""
    from database import get_db

    db = None
    try:
        db = get_db()
        version = db.fetch_one("select max(version) as version from schema_version")
        if not version or version["version"] != 1:
            return jsonify({"status": "error", "database": "unavailable"}), 503
        return jsonify({"status": "ok", "database": "ok"})
    except Exception:
        return jsonify({"status": "error", "database": "unavailable"}), 503
    finally:
        if db is not None:
            db.close()


@app.errorhandler(psycopg2.OperationalError)
def database_unavailable(error):
    """Return an error when the database cannot be reached."""
    return jsonify({"error": "database temporarily unavailable"}), 503


@app.errorhandler(psycopg2.IntegrityError)
def invalid_database_write(error):
    """Return an error when database data breaks a rule."""
    return jsonify({"error": "data conflicts with existing records or database constraints"}), 409


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
