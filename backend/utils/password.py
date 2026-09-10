"""Password/JWT utilities independent of HTTP."""

from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from config import JWT_ALGORITHM, JWT_EXPIRE_HOURS, JWT_SECRET


def hash_password(password):
    """Hash the password with bcrypt and a random salt before storing it in the database."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, password_hash):
    """Compare the entered password with the stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def make_token(user):
    """Issue a JWT containing the user ID, role, and configured expiration time."""
    payload = {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
