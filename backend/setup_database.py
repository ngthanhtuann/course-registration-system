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

        with db.conn.cursor() as cursor:
            cursor.execute("select to_regclass('users'), to_regclass('schema_version')")
            users_table, version_table = cursor.fetchone()
            if users_table is None and version_table is None:
                cursor.execute(sql)
            elif users_table is not None and version_table is not None:
                # Upgrade the existing schema without rebuilding or deleting data.
                cursor.execute("select max(version) from schema_version")
                version = cursor.fetchone()[0]
                if version not in (1, 2):
                    raise RuntimeError("Unsupported database schema version")
                cursor.execute("""
                    alter table users
                        add column if not exists failed_login_attempts integer
                            not null default 0 check (failed_login_attempts >= 0),
                        add column if not exists locked_until timestamptz,
                        add column if not exists token_version bigint
                            not null default 0 check (token_version >= 0);
                    insert into schema_version(version) values (2)
                        on conflict (version) do nothing;
                """)
            else:
                raise RuntimeError("Incomplete database schema; setup cannot safely proceed")

        db.conn.commit()

        print("Database setup successfully.")

    except Exception as error:
        db.conn.rollback()
        print("Database setup failed:", error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    setup_database()
