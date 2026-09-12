import getpass
import re

from utils.password import hash_password
from database import get_db


def main():
    """Create the first administrator account."""

    user_id = input("Admin ID: ").strip()
    full_name = input("Full name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password (8+ characters): ")

    if (not user_id or len(user_id) > 20 or not full_name or len(full_name) > 100
            or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email)
            or len(email) > 100 or not 8 <= len(password.encode("utf-8")) <= 72):
        raise SystemExit(
            "Use ID <=20 characters, name <=100, valid email <=100, and password 8-72 UTF-8 bytes."
        )

    username = user_id.lower()

    db = get_db()

    try:
        db.fetch_one("select pg_advisory_xact_lock(714230902)")
        if db.fetch_one("select 1 from users where role='admin' limit 1"):
            print("An administrator already exists. No new account was created.")
            return
        exists = db.fetch_one(
            """
            select 1
            from users
            where user_id = %s
               or username = %s
               or email = %s
            """,
            (user_id, username, email),
        )

        if exists:
            raise SystemExit(
                "An account with this ID, username, or email already exists."
            )

        password_hash = hash_password(password)

        db.execute(
            """
            insert into users (
                user_id,
                username,
                password_hash,
                full_name,
                email,
                role,
                active_status
            )
            values (%s, %s, %s, %s, %s, 'admin', true)
            """,
            (
                user_id,
                username,
                password_hash,
                full_name,
                email,
            ),
        )

        db.execute(
            """
            insert into administrators (
                admin_id,
                user_id
            )
            values (%s, %s)
            """,
            (user_id, user_id),
        )

        db.conn.commit()

        print("Administrator account created successfully.")
        print(f"Username: {username}")

    except Exception:
        db.conn.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()