"""Tiện ích mật khẩu/JWT độc lập với HTTP."""

from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from config import JWT_ALGORITHM, JWT_EXPIRE_HOURS, JWT_SECRET


def hash_password(password):
    """Băm mật khẩu bằng bcrypt cùng salt ngẫu nhiên trước khi lưu database."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, password_hash):
    """So sánh mật khẩu nhập vào với chuỗi băm đã lưu bằng bcrypt."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def make_token(user):
    """Cấp JWT chứa mã người dùng, vai trò và thời gian hết hạn theo cấu hình."""
    payload = {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
