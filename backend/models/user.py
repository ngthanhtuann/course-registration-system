"""Functions shared by all users."""

from database import get_db
from utils.password import hash_password, check_password, make_token
import re

_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _required_text(value, field_name):
    """Return a trimmed non-empty string or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    return value


def _valid_email(value):
    """Validate and normalize an email address."""
    email = _required_text(value, "Email")
    if not _EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email address")
    return email


class User:
    """Common functions for Admin, Lecturer, and Student users."""

    def __init__(self, identity=None):
        """Create a User object from user information."""
        if identity is None:
            identity = {}

        self.identity = dict(identity)

        self.userId = self.identity.get("user_id")
        self.username = self.identity.get("username", "")
        self.fullName = self.identity.get(
            "full_name",
            self.identity.get("fullname", "")
        )
        self.email = self.identity.get("email", "")
        self.role = self.identity.get("role", "")
        self._passwordHash = None

    def _loadAccount(self, row):
        """Copy account data from a database row to this object."""

        self.userId = row.get("user_id", self.userId)
        self.username = row.get("username", self.username)

        self.fullName = row.get(
            "full_name",
            row.get("fullname", self.fullName)
        )

        self.email = row.get("email", self.email)
        self.role = row.get("role", self.role)

        self._passwordHash = row.get(
            "password_hash",
            row.get("password", self._passwordHash)
        )

        self.identity.update(
            {
                "user_id": self.userId,
                "username": self.username,
                "fullname": self.fullName,
                "full_name": self.fullName,
                "email": self.email,
                "role": self.role,
            }
        )

    def _loadLoginUser(self, db, username):
        """Find a user account and role-specific profile in one query."""
        return db.fetch_one(
            """
            select
                u.user_id,
                u.username,
                u.password_hash,
                u.password_hash as password,
                u.full_name,
                u.full_name as fullname,
                u.email,
                lower(u.role::text) as role,
                u.active_status,
                s.student_id,
                s.major_code,
                l.lecturer_id,
                coalesce(
                    array_agg(distinct q.course_code)
                    filter (where q.course_code is not null),
                    '{}'
                ) as qualifications
            from users u
            left join students s on s.user_id = u.user_id
            left join lecturers l on l.user_id = u.user_id
            left join lecturer_qualifications q on q.lecturer_id = l.lecturer_id
            where u.username = %s
            group by u.user_id, s.student_id, s.major_code, l.lecturer_id
            """,
            (username,),
        )

    def _authUserPayload(self, user):
        """Build the frontend user payload without another profile request."""
        payload = {
            "user_id": user["user_id"],
            "username": user["username"],
            "fullname": user["full_name"],
            "email": user["email"],
            "role": user["role"],
        }

        if user["role"] == "student":
            payload["student_id"] = user.get("student_id")
            payload["major_code"] = user.get("major_code")
        elif user["role"] == "lecturer":
            payload["lecturer_id"] = user.get("lecturer_id")
            payload["qualifications"] = user.get("qualifications") or []

        return payload

    def login(self, data):
        """Check username and password and return a login token."""
        data = data or {}
        username = data.get("username", "")
        password = data.get("password", "")

        if not isinstance(username, str) or not isinstance(password, str):
            return ({"error": "username and password must be strings"}, 400)

        username = username.strip()
        if not username or not password:
            return ({"error": "username and password are required"}, 400)

        db = get_db()
        try:
            user = self._loadLoginUser(db, username)
            valid_password = False

            if user:
                try:
                    valid_password = check_password(password, user["password_hash"])
                except (ValueError, TypeError):
                    valid_password = False

            if (
                not user
                or not user.get("active_status", True)
                or not valid_password
            ):
                return ({"error": "invalid username or password"}, 401)

            token = make_token(user)
            self._loadAccount(user)

            return {
                "token": token,
                "user": self._authUserPayload(user),
            }
        finally:
            db.close()

    def viewAccountInfo(self):
        """Get account and role-specific profile information in one query."""
        user = self.identity
        db = get_db()

        try:
            result = db.fetch_one(
                """
                select
                    u.user_id,
                    u.username,
                    u.full_name,
                    u.full_name as fullname,
                    u.email,
                    lower(u.role::text) as role,
                    u.active_status,
                    s.student_id,
                    s.major_code,
                    l.lecturer_id,
                    coalesce(
                        array_agg(distinct q.course_code)
                        filter (where q.course_code is not null),
                        '{}'
                    ) as qualifications
                from users u
                left join students s on s.user_id = u.user_id
                left join lecturers l on l.user_id = u.user_id
                left join lecturer_qualifications q on q.lecturer_id = l.lecturer_id
                where u.user_id = %s
                group by u.user_id, s.student_id, s.major_code, l.lecturer_id
                """,
                (user["user_id"],),
            )

            if not result:
                return ({"error": "account not found"}, 404)

            self._loadAccount(result)
            return (self._authUserPayload(result), 200)
        finally:
            db.close()

    def updateProfile(self, data):
        """Update the user full name and email."""

        data = data or {}

        try:
            fullname = _required_text(
                data.get("fullname", data.get("full_name")),
                "Full name",
            )
            email = _valid_email(data.get("email"))
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        user = self.identity
        db = get_db()

        try:
            duplicate = db.fetch_one(
                """
                select user_id
                from users
                where email = %s
                  and user_id <> %s
                """,
                (email, user["user_id"]),
            )

            if duplicate:
                return (
                    {"error": "Email already exists"},
                    409,
                )

            db.execute(
                """
                update users
                set full_name = %s,
                    email = %s
                where user_id = %s
                """,
                (
                    fullname,
                    email,
                    user["user_id"],
                ),
            )

            db.conn.commit()

            self._loadAccount(
                {
                    "full_name": fullname,
                    "fullname": fullname,
                    "email": email,
                }
            )

            return {
                "message": "profile updated successfully"
            }

        except Exception:
            db.conn.rollback()
            raise

        finally:
            db.close()

    def changePassword(self, data):
        """Check the old password and save a new password."""

        data = data or {}

        current = data.get("current_password", "")
        new_password = data.get("new_password", "")

        if not isinstance(current, str) or not isinstance(new_password, str):
            return (
                {
                    "error":
                    "current_password and new_password must be strings"
                },
                400,
            )

        if not current or not new_password:
            return (
                {
                    "error":
                    "current_password and new_password are required"
                },
                400,
            )

        if len(new_password) < 8:
            return (
                {
                    "error":
                    "new password must contain at least 8 characters"
                },
                400,
            )

        user = self.identity
        db = get_db()

        try:
            row = self._loadLoginUser(
                db,
                user["username"],
            )

            if (
                not row
                or not check_password(
                    current,
                    row["password_hash"],
                )
            ):
                return (
                    {
                        "error":
                        "current password is incorrect"
                    },
                    400,
                )

            password_hash = hash_password(
                new_password
            )

            db.execute(
                """
                update users
                set password_hash = %s
                where user_id = %s
                """,
                (
                    password_hash,
                    user["user_id"],
                ),
            )

            db.conn.commit()

            return {
                "message": "password changed successfully"
            }

        except Exception:
            db.conn.rollback()
            raise

        finally:
            db.close()

    def logout(self):
        """Return a logout success message."""

        self.identity.clear()

        self.userId = None
        self.username = ""
        self.fullName = ""
        self.email = ""
        self.role = ""
        self._passwordHash = None

        return {
            "message": "logged out successfully"
        }
