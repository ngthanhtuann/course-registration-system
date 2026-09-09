"""Tiện ích kiểm tra quyền tại API Flask."""

from functools import wraps
import jwt
from flask import jsonify, request
from config import JWT_ALGORITHM, JWT_SECRET
from database import get_db


def get_current_user():
    """Giải mã Bearer JWT hợp lệ; trả None nếu token hết hạn hoặc không hợp lệ."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    try:
        payload = jwt.decode(
            header.split(" ", 1)[1], JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth(*roles):
    """Tạo bộ kiểm tra đăng nhập, vai trò và trạng thái hoạt động trước khi gọi API."""

    def decorator(fn):
        """Gắn kiểm tra quyền vào hàm API và giữ lại tên hàm bằng wraps."""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            """Từ chối truy cập trái quyền hoặc tài khoản bị khóa trước khi chạy nghiệp vụ."""
            user = get_current_user()
            if not user:
                return (jsonify({"error": "authentication required"}), 401)
            if roles and user["role"] not in roles:
                return (jsonify({"error": "forbidden"}), 403)
            db = get_db()
            try:
                active = db.fetch_one(
                    "select active_status from users where user_id=%s",
                    (user["user_id"],),
                )
                if not active or not active.get("active_status", True):
                    return (jsonify({"error": "account is inactive"}), 403)
            finally:
                db.close()
            return fn(*args, **kwargs)

        return wrapper

    return decorator
