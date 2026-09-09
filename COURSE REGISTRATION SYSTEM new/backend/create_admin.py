import getpass
from credentials import hash_password
from database import get_db


def main():
    """Nhập tài khoản quản trị ban đầu và tạo hai bản ghi trong cùng giao dịch."""
    user_id = input("Admin ID: ").strip()
    fullname = input("Full name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password (8+ characters): ")
    if not user_id or not fullname or not email or len(password) < 8:
        raise SystemExit(
            "All fields are required and password must be at least 8 characters."
        )
    db = get_db()
    try:
        exists = db.fetch_one(
            "select 1 from users where user_id=%s or username=%s or email=%s",
            (user_id, user_id.lower(), email),
        )
        if exists:
            raise SystemExit(
                "An account with this ID, username, or email already exists."
            )
        password_hash = hash_password(password)
        db.execute(
            "insert into users (user_id, username, password, password_hash, fullname, email, role) values (%s,%s,%s,%s,%s,%s,'admin')",
            (user_id, user_id.lower(), password_hash, password_hash, fullname, email),
        )
        db.execute(
            "insert into administrators (admin_id, user_id) values (%s,%s)",
            (user_id, user_id),
        )
        db.conn.commit()
        print("Administrator account created successfully.")
    except Exception:
        db.conn.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
