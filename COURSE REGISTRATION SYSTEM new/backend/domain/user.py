"""Nghiệp vụ hướng đối tượng cho vai trò User."""

from database import get_db
from credentials import hash_password, check_password, make_token


class User:
    """User: đóng gói nghiệp vụ theo Class Diagram; không phụ thuộc Flask."""

    def __init__(self, identity=None):
        """Lưu danh tính đã được API xác thực; không giữ mật khẩu dạng rõ trong đối tượng."""
        if identity is None:
            identity = {}
        self.identity = dict(identity)
        self.userId = self.identity.get("user_id")
        self.username = self.identity.get("username", "")
        self.fullName = self.identity.get("fullname", "")
        self.email = self.identity.get("email", "")
        self.role = self.identity.get("role", "")
        self._passwordHash = None

    def _loadAccount(self, row):
        """Đồng bộ thuộc tính đối tượng từ bản ghi tài khoản; chỉ giữ mật khẩu đã băm."""
        self.userId = row.get("user_id", self.userId)
        self.username = row.get("username", self.username)
        self.fullName = row.get("fullname", self.fullName)
        self.email = row.get("email", self.email)
        self.role = row.get("role", self.role)
        self._passwordHash = row.get("password", self._passwordHash)
        self.identity.update(
            {
                "user_id": self.userId,
                "username": self.username,
                "fullname": self.fullName,
                "email": self.email,
                "role": self.role,
            }
        )

    def _loadLoginUser(self, db, username):
        """Đọc tài khoản từ schema hiện tại hoặc schema cũ mà không di chuyển dữ liệu."""
        columns = db.fetch_all(
            """
            select column_name
            from information_schema.columns
            where table_schema=current_schema() and table_name='users'
            """
        )
        column_names = {row["column_name"] for row in columns}
        if "password" in column_names:
            return db.fetch_one(
                """
                  select user_id, username, password, fullname, email, lower(role::text) as role,
                      active_status
                from users
                where username = %s
                """,
                (username,),
            )
        return db.fetch_one(
            """
            select u.user_id, u.username, u.password_hash as password,
                   coalesce(s.full_name, l.full_name, u.username) as fullname,
                   coalesce(s.email, l.email) as email,
                   lower(u.role::text) as role,
                   (u.account_status::text = 'ACTIVE') and coalesce(u.active_status, true)
                   as active_status
            from users u
            left join students s on s.user_id=u.user_id
            left join lecturers l on l.user_id=u.user_id
            where u.username = %s
            """,
            (username,),
        )

    def login(self, data):
        """Xác thực tài khoản đang hoạt động và cấp token đăng nhập."""
        data = data or {}
        username = data.get("username", "").strip()
        password = data.get("password", "")
        if not username or not password:
            return ({"error": "username and password are required"}, 400)
        db = get_db()
        try:
            user = self._loadLoginUser(db, username)
            valid_password = False
            if user:
                try:
                    valid_password = check_password(password, user["password"])
                except (ValueError, TypeError):
                    valid_password = False
            if not user or not user.get("active_status", True) or (not valid_password):
                return ({"error": "invalid username or password"}, 401)
            token = make_token(user)
            self._loadAccount(user)
            return {
                "token": token,
                "user": {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "fullname": user["fullname"],
                    "email": user["email"],
                    "role": user["role"],
                },
            }
        finally:
            db.close()

    def viewAccountInfo(self):
        """Đọc thông tin tài khoản của người dùng hiện tại."""
        user = self.identity
        db = get_db()
        try:
            columns = db.fetch_all(
                """
                select column_name
                from information_schema.columns
                where table_schema=current_schema() and table_name='users'
                """
            )
            column_names = {row["column_name"] for row in columns}
            if "password" in column_names:
                result = db.fetch_one(
                    """
                    select user_id, username, fullname, email, lower(role::text) as role
                    from users where user_id = %s
                    """,
                    (user["user_id"],),
                )
            else:
                result = db.fetch_one(
                    """
                    select u.user_id, u.username,
                           coalesce(s.full_name, l.full_name, u.username) as fullname,
                           coalesce(s.email, l.email) as email,
                           lower(u.role::text) as role
                    from users u
                    left join students s on s.user_id=u.user_id
                    left join lecturers l on l.user_id=u.user_id
                    where u.user_id = %s
                    """,
                    (user["user_id"],),
                )
            if result:
                self._loadAccount(result)
            return (result or {}, 200)
        finally:
            db.close()

    def updateProfile(self, data):
        """Cập nhật họ tên, email và kiểm tra email bị trùng."""
        data = data or {}
        fullname = (data.get("fullname") or "").strip()
        email = (data.get("email") or "").strip()
        if not fullname or not email:
            return ({"error": "fullname and email are required"}, 400)
        user = self.identity
        db = get_db()
        try:
            duplicate = db.fetch_one(
                "select user_id from users where email=%s and user_id<>%s",
                (email, user["user_id"]),
            )
            if duplicate:
                return ({"error": "Email already exists"}, 409)
            db.execute(
                "update users set fullname=%s, email=%s where user_id=%s",
                (fullname, email, user["user_id"]),
            )
            db.execute(
                "update students set full_name=%s, email=%s where user_id=%s",
                (fullname, email, user["user_id"]),
            )
            db.execute(
                "update lecturers set full_name=%s, fullname=%s, email=%s where user_id=%s",
                (fullname, fullname, email, user["user_id"]),
            )
            db.conn.commit()
            self._loadAccount({"fullname": fullname, "email": email})
            return {"message": "profile updated successfully"}
        finally:
            db.close()

    def changePassword(self, data):
        """Kiểm tra mật khẩu cũ rồi lưu mật khẩu mới dưới dạng băm."""
        data = data or {}
        current = data.get("current_password", "")
        new_password = data.get("new_password", "")
        if not current or not new_password:
            return ({"error": "current_password and new_password are required"}, 400)
        if len(new_password) < 8:
            return ({"error": "new password must contain at least 8 characters"}, 400)
        user = self.identity
        db = get_db()
        try:
            row = self._loadLoginUser(db, user["username"])
            if not row or not check_password(current, row["password"]):
                return ({"error": "current password is incorrect"}, 400)
            password_hash = hash_password(new_password)
            db.execute_query(
                "update users set password = %s, password_hash = %s where user_id = %s",
                (password_hash, password_hash, user["user_id"]),
            )
            return {"message": "password changed successfully"}
        finally:
            db.close()

    def logout(self):
        """Kết thúc phiên phía client: yêu cầu xóa JWT; token đã cấp vẫn hết hạn theo cấu hình."""
        self.identity.clear()
        self.userId = None
        self.username = ""
        self.fullName = ""
        self.email = ""
        self.role = ""
        self._passwordHash = None
        return {"message": "logged out successfully"}
