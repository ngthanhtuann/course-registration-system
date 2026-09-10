from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.user_routes import admin_bp
from routes.student_routes import student_bp
from routes.teaching_routes import lecturer_bp

from utils.http_support import ISOJSONProvider

app = Flask(__name__)
app.json = ISOJSONProvider(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(lecturer_bp)


@app.get("/")
def home():
    """Return a backend identification message at the root URL."""
    return jsonify({"message": "course registration system backend is running"})


@app.get("/api/health")
def health():
    """Return database readiness, using HTTP 503 when PostgreSQL is unavailable."""
    from database import get_db

    db = None
    try:
        db = get_db()
        db.fetch_one("select 1 as ready")
        return jsonify({"status": "ok", "database": "ok"})
    except Exception:
        return jsonify({"status": "error", "database": "unavailable"}), 503
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
