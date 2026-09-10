"""Exercise real API writes in an isolated PostgreSQL schema, removed in finally.

Run with the backend virtualenv: python backend/checks/integration_check.py
Optional --legacy-dump PATH uses a schema-only pg_dump of the migrated database.
No application rows in the existing schema are modified.
"""
import argparse
from datetime import date, timedelta
from pathlib import Path
import re
import sys
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database
from psycopg2 import sql
from app import app
import create_admin


def run(dump=None, migration=None):
    """Create isolated tables and check persisted results across separate connections."""
    schema = "crs_check_" + uuid4().hex
    control = database.get_db()
    control.conn.autocommit = True
    original_connect = database.psycopg2.connect
    calls = 0

    def connect(*args, **kwargs):
        """Force every application connection into the isolated schema only."""
        kwargs["options"] = "-c search_path=" + schema
        return original_connect(*args, **kwargs)

    def request(method, path, token=None, data=None, status=200):
        """Assert the API result without printing credentials or tokens."""
        nonlocal calls
        headers = {"Authorization": "Bearer " + token} if token else {}
        response = client.open(path, method=method, headers=headers, json=data)
        assert response.status_code == status, (method, path, response.status_code, response.get_json())
        calls += 1
        return response.get_json()

    def login(username, password="TestPassword123!"):
        """Authenticate through the real bcrypt and JWT login flow."""
        return request("POST", "/api/login", data={"username": username, "password": password})["token"]

    def query(statement, params=None):
        """Read committed state using a new connection after each API request."""
        db = database.get_db()
        try:
            return db.fetch_one(statement, params)
        finally:
            db.close()

    try:
        control.conn.cursor().execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
        with patch.object(database.psycopg2, "connect", connect):
            db = database.get_db()
            try:
                if dump:
                    source = Path(dump).read_text(encoding="utf-8")
                    source = re.sub(r"^\\.*$", "", source, flags=re.M)
                    source = source.replace("public", schema)
                    source = re.sub(r"CREATE SCHEMA " + schema + r";", "", source)
                else:
                    source = (Path(__file__).resolve().parents[2] / "database" / "schema.sql").read_text()
                db.conn.cursor().execute(source)
                if dump:
                    db.conn.cursor().execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
                    db.conn.cursor().execute((Path(__file__).resolve().parents[1] / "migrations/003_administrators_compatibility.sql").read_text())
                if migration:
                    db.conn.cursor().execute(Path(migration).read_text())
                db.conn.commit()
            finally:
                db.close()
            app.config["TESTING"] = True
            client = app.test_client()
            with patch("builtins.input", side_effect=["TESTADMIN", "Test Admin", "admin@example.invalid"]), patch("getpass.getpass", return_value="TestPassword123!"):
                create_admin.main()
            admin = login("testadmin")
            request("GET", "/api/health")
            request("POST", "/api/admin/majors", admin, {"major_code": "TEST", "major_name": "Test Major"}, 201)
            request("POST", "/api/admin/courses", admin, {"course_code": "C1", "course_name": "Test Course", "credit": 3, "max_capacity": 10}, 201)
            request("POST", "/api/admin/curriculum", admin, {"major_code": "TEST", "course_code": "C1", "recommended_semester": "1"}, 201)
            for role, uid in [("student", "ST1"), ("lecturer", "LE1")]:
                request("POST", "/api/admin/users", admin, {"user_id": uid, "fullname": "Test User", "email": uid + "@example.invalid", "password": "TestPassword123!", "role": role, "major_code": "TEST", "dob": "2000-01-01", "qualifications": ["C1"]}, 201)
                token = login(uid.lower())
                request("PUT", "/api/account/profile", token, {"fullname": "Updated Name", "email": uid + "new@example.invalid"})
                table = "students" if role == "student" else "lecturers"
                row = query("select u.full_name,u.email from users u join " + table + " p on p.user_id=u.user_id where u.user_id=%s", (uid,))
                assert row["full_name"] == "Updated Name"
                assert row["email"] == uid + "new@example.invalid"
                request("PUT", "/api/admin/users/" + uid, admin, {"fullname": "Admin Updated"})
                assert query("select full_name from users where user_id=%s", (uid,))["full_name"] == "Admin Updated"
                request("PUT", "/api/account/password", token, {"current_password": "TestPassword123!", "new_password": "ChangedPassword123!"})
                login(uid.lower(), "ChangedPassword123!")
                request("POST", "/api/login", data={"username": uid.lower(), "password": "TestPassword123!"}, status=401)
            # A failure after updating the account must roll back the whole admin edit.
            student = login("st1", "ChangedPassword123!")
            old_execute = database.Database.execute
            def fail_profile(self, statement, params=None):
                """Inject failure in the profile write to verify account rollback."""
                if "update students" in statement:
                    raise RuntimeError("injected profile failure")
                return old_execute(self, statement, params)
            with patch.object(database.Database, "execute", fail_profile):
                request("PUT", "/api/admin/users/ST1", admin,
                        {"fullname": "Must Roll Back", "major_code": "TEST"}, 400)
            assert query("select full_name from users where user_id='ST1'")["full_name"] == "Admin Updated"
            today = date.today()
            start, end = (today - timedelta(days=30)).isoformat(), (today + timedelta(days=30)).isoformat()
            request("POST", "/api/admin/semesters", admin, {"semester_id": "SEM1", "semester_name": "Test Semester", "start_date": start, "end_date": end}, 201)
            semesters = request("GET", "/api/admin/semesters", admin)
            assert semesters[0]["start_date"][:10] == start
            period = {"period_id": "PER1", "semester_id": "SEM1", "period_name": "Test Period", "start_date": start, "end_date": end}
            request("POST", "/api/admin/registration-periods", admin, {**period, "start_date": (today - timedelta(days=40)).isoformat()}, 400)
            request("POST", "/api/admin/registration-periods", admin, period, 201)
            request("POST", "/api/admin/teaching-assignments", admin, {"semester_id": "SEM1", "lecturer_id": "LE1", "course_code": "C1"}, 201)
            reg = request("POST", "/api/student/registrations", student, {"course_code": "C1", "period_id": "PER1"}, 201)["registration_id"]
            request("POST", "/api/student/registrations", student, {"course_code": "C1", "period_id": "PER1"}, 409)
            request("PUT", "/api/student/registrations/" + reg + "/drop", student)
            request("POST", "/api/student/registrations", student, {"course_code": "C1", "period_id": "PER1"}, 201)
            lecturer = login("le1", "ChangedPassword123!")
            request("PUT", "/api/lecturer/registrations/" + reg + "/grade", lecturer, {"grade": 8}, 400)
            request("PUT", "/api/admin/registration-periods/PER1", admin, {**period, "end_date": (today - timedelta(days=1)).isoformat()})
            request("PUT", "/api/lecturer/registrations/" + reg + "/grade", lecturer, {"grade": 8})
            grades = request("GET", "/api/student/grades", student)
            assert any(float(row["grade"]) == 8 for row in grades)
            # Every read endpoint runs against populated canonical tables.
            for path in ["dashboard", "users", "majors", "courses", "curriculum/TEST", "semesters",
                         "registration-periods", "registration-demand?period_id=PER1&major_code=TEST",
                         "registration-demand/C1/students?period_id=PER1", "teaching-assignments?semester_id=SEM1",
                         "qualified-lecturers/C1"]:
                request("GET", "/api/admin/" + path, admin)
            for path in ["profile", "semesters", "registration-periods", "curriculum", "courses?period_id=PER1",
                         "registrations?semester_id=SEM1", "grades?semester_id=SEM1"]:
                request("GET", "/api/student/" + path, student)
            for path in ["profile", "semesters", "teaching-courses?semester_id=SEM1", "courses/C1/students?semester_id=SEM1"]:
                request("GET", "/api/lecturer/" + path, lecturer)
            # Exercise the remaining writes and verify API aliases after normalization.
            request("GET", "/api/me", admin)
            assert request("GET", "/api/student/profile", student)["fullname"] == "Admin Updated"
            assert request("GET", "/api/lecturer/profile", lecturer)["qualifications"] == ["C1"]
            curriculum = request("GET", "/api/admin/curriculum/TEST", admin)
            assert curriculum[0]["course_code"] == "C1" and "prerequisite_course_code" in curriculum[0]
            request("PUT", "/api/admin/users/ST1", admin, {"major_code": "TEST"})
            request("PUT", "/api/admin/users/LE1", admin, {"qualifications": ["C1"]})
            request("PUT", "/api/admin/majors/TEST", admin, {"major_name": "Updated Major"})
            request("PUT", "/api/admin/courses/C1", admin, {"course_name": "Updated Course", "credit": 4, "max_capacity": 12})
            request("POST", "/api/admin/courses", admin, {"course_code": "C2", "course_name": "Next Course", "credit": 3, "max_capacity": 10, "prerequisite_course_code": "C1"}, 201)
            courses = request("GET", "/api/admin/courses", admin)
            assert next(c for c in courses if c["course_code"] == "C2")["prerequisite_course_code"] == "C1"
            request("POST", "/api/admin/courses", admin, {"course_code": "BAD", "course_name": "Invalid", "credit": 3, "max_capacity": 10, "prerequisite_course_code": "MISSING"}, 400)
            request("POST", "/api/admin/curriculum", admin, {"curriculum_id": "CU2", "major_code": "TEST", "course_code": "C2"}, 201)
            request("PUT", "/api/admin/curriculum/CU2", admin, {"recommended_semester": "2"})
            request("POST", "/api/admin/lecturer-qualifications", admin, {"lecturer_id": "LE1", "course_code": "C2"}, 201)
            request("POST", "/api/admin/teaching-assignments", admin, {"assignment_id": "TA2", "lecturer_id": "LE1", "course_code": "C2", "semester_id": "SEM1"}, 201)
            request("DELETE", "/api/admin/teaching-assignments/TA2", admin)
            request("DELETE", "/api/admin/lecturer-qualifications/LE1/C2", admin)
            request("DELETE", "/api/admin/curriculum/CU2", admin)
            request("DELETE", "/api/admin/courses/C2", admin)
            request("POST", "/api/admin/majors", admin, {"major_code": "EMPTY", "major_name": "Empty Major"}, 201)
            request("DELETE", "/api/admin/majors/EMPTY", admin)
            future_start = (today + timedelta(days=100)).isoformat()
            future_end = (today + timedelta(days=130)).isoformat()
            semester_data = {"semester_id": "SEM2", "semester_name": "Future", "start_date": future_start, "end_date": future_end}
            request("POST", "/api/admin/semesters", admin, semester_data, 201)
            request("PUT", "/api/admin/semesters/SEM2", admin, semester_data)
            request("POST", "/api/admin/registration-periods", admin, {"period_id": "PER2", "semester_id": "SEM2", "start_date": future_start, "end_date": future_end}, 201)
            request("DELETE", "/api/admin/registration-periods/PER2", admin)
            request("DELETE", "/api/admin/semesters/SEM2", admin)
            request("DELETE", "/api/admin/users/ST1", admin)
            request("POST", "/api/login", data={"username": "st1", "password": "ChangedPassword123!"}, status=401)
            request("GET", "/api/student/profile", student, status=403)
            request("GET", "/api/admin/users", student, status=403)
            request("GET", "/api/admin/users", status=401)
            with patch.object(database, "get_db", side_effect=RuntimeError("database offline")):
                request("GET", "/api/health", status=503)
            print(f"INTEGRATION PASS: {calls} API assertions; persisted profiles, rollback, login/password, registration/drop/re-register, grades, permissions, health")
    finally:
        control.conn.cursor().execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))
        control.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-dump")
    parser.add_argument("--migration")
    args = parser.parse_args()
    run(args.legacy_dump, args.migration)
