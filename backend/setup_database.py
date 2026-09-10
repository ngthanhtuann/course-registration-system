import os
from pathlib import Path

from database import get_db


def setup_database():
    direct_url = os.getenv("DIRECT_DATABASE_URL", "").strip()

    if direct_url:
        os.environ["DATABASE_URL"] = direct_url

    db = get_db()

    try:
        schema_path = Path(__file__).resolve().parents[1] / "database" / "schema.sql"

        with open(schema_path, "r") as file:
            sql = file.read()

        cursor = db.conn.cursor()
        cursor.execute(sql)

        db.conn.commit()

        print("Database setup successfully.")

    except Exception as error:
        db.conn.rollback()
        print("Database setup failed:", error)

    finally:
        db.close()


if __name__ == "__main__":
    setup_database()