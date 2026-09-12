"""Authorization utilities for the Flask API."""

from functools import wraps
from threading import Lock
from time import time
import jwt
from flask import jsonify, request
from config import JWT_ALGORITHM, JWT_SECRET
from database import get_db

# Single-process demo only. Production multi-instance needs a shared Redis/DB denylist.
revoked_tokens = {}
_revoked_lock = Lock()


def revoke_current_token(payload):
    token = request.headers.get("Authorization", "").split(" ", 1)[1]
    with _revoked_lock:
        revoked_tokens[token] = payload.get("exp")


def is_token_revoked(token):
    with _revoked_lock:
        now = time()
        for saved_token, expires in list(revoked_tokens.items()):
            if expires is not None and expires <= now:
                del revoked_tokens[saved_token]
        return token in revoked_tokens


def get_current_user():
    """Decode a valid Bearer JWT; return None if the token is expired or invalid."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header.split(" ", 1)[1]
    if is_token_revoked(token):
        return None
    try:
        payload = jwt.decode(
            header.split(" ", 1)[1], JWT_SECRET, algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "user_id", "username", "role", "token_version"]},
        )
        if (
            not all(isinstance(payload.get(key), str) and payload[key]
                    for key in ("user_id", "username", "role"))
            or type(payload.get("token_version")) is not int
            or payload["token_version"] < 0
        ):
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth(*roles):
    """Create checks for login, role, and active status before calling the API."""

    def decorator(fn):
        """Attach authorization checks to the API function and preserve its name with wraps."""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            """Reject unauthorized access or locked accounts before running business logic."""
            user = get_current_user()
            if not user:
                return (jsonify({"error": "authentication required"}), 401)
            if roles and user["role"] not in roles:
                return (jsonify({"error": "forbidden"}), 403)
            db = get_db()
            try:
                active = db.fetch_one(
                    "select active_status, token_version, role from users where user_id=%s",
                    (user["user_id"],),
                )
                if not active or not active.get("active_status", True):
                    return (jsonify({"error": "account is inactive"}), 403)
                if (active["token_version"] != user["token_version"]
                        or active["role"] != user["role"]):
                    return (jsonify({"error": "session has been revoked; please log in again"}), 401)
            finally:
                db.close()
            return fn(*args, **kwargs)

        return wrapper

    return decorator
