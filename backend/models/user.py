"""Object-oriented business logic for the User role."""

from database import get_db
from utils.password import hash_password, check_password, make_token


class User:
    """User: encapsulates business logic according to the Class Diagram; independent of Flask."""

    def __init__(self, identity=None):
        """Store the identity authenticated by the API; do not keep plaintext passwords in the object."""
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
        """Synchronize object attributes from the account record."""

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
        """Read the login account from the users table."""

        return db.fetch_one(
            """
            select
                user_id,
                username,
                password_hash,
                password_hash as password,
                full_name,
                full_name as fullname,
                email,
                lower(role::text) as role,
                active_status
            from users
            where username = %s
            """,
            (username,),
        )

    def login(self, data):
        """Authenticate an active account and issue a login token."""

        data = data or {}

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return (
                {"error": "username and password are required"},
                400,
            )

        db = get_db()

        try:
            user = self._loadLoginUser(db, username)

            valid_password = False

            if user:
                try:
                    valid_password = check_password(
                        password,
                        user["password_hash"],
                    )
                except (ValueError, TypeError):
                    valid_password = False

            if (
                not user
                or not user.get("active_status", True)
                or not valid_password
            ):
                return (
                    {"error": "invalid username or password"},
                    401,
                )

            token = make_token(user)

            self._loadAccount(user)

            return {
                "token": token,
                "user": {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "fullname": user["full_name"],
                    "email": user["email"],
                    "role": user["role"],
                },
            }

        finally:
            db.close()

    def viewAccountInfo(self):
        """Read the current user’s account information."""

        user = self.identity
        db = get_db()

        try:
            result = db.fetch_one(
                """
                select
                    user_id,
                    username,
                    full_name,
                    full_name as fullname,
                    email,
                    lower(role::text) as role,
                    active_status
                from users
                where user_id = %s
                """,
                (user["user_id"],),
            )

            if result:
                self._loadAccount(result)

            return (result or {}, 200)

        finally:
            db.close()

    def updateProfile(self, data):
        """Update full name and email, and check for duplicate email addresses."""

        data = data or {}

        fullname = (
            data.get("fullname")
            or data.get("full_name")
            or ""
        ).strip()

        email = (data.get("email") or "").strip()

        if not fullname or not email:
            return (
                {"error": "fullname and email are required"},
                400,
            )

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
        """Verify the old password, then store the new password as a hash."""

        data = data or {}

        current = data.get("current_password", "")
        new_password = data.get("new_password", "")

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
        """End the session on the client side."""

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