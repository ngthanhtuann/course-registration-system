import getpass

from utils.password import hash_password
from database import get_db


def main():
    """Prompt for the initial administrator account and create both records in the same transaction."""

    user_id = input("Admin ID: ").strip()
    full_name = input("Full name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password (8+ characters): ")

    if not user_id or not full_name or not email or len(password) < 8:
        raise SystemExit(
            "All fields are required and password must be at least 8 characters."
        )

    username = user_id.lower()

    db = get_db()

    try:
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