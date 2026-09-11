"""Read-only model benchmark. No login, tokens, schema changes or writes.

Run from backend: ../.venv/Scripts/python tests/profile_reads.py OUTPUT.json
Times exclude HTTP/auth unless the operation explicitly says health/auth-status.
Only aggregate timings are saved, never rows or SQL parameters.
"""
import json
import statistics
import sys
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import psycopg2
import database
from main import app
from models.admin import Administrator
from models.student import Student
from models.lecturer import Lecturer
from models.user import User


def main():
    original_connect = psycopg2.connect

    def readonly_connect(*args, **kwargs):
        kwargs["options"] = "-c default_transaction_read_only=on"
        return original_connect(*args, **kwargs)

    with patch.object(psycopg2, "connect", readonly_connect):
        start = perf_counter()
        db = database.get_db()
        cold_ms = (perf_counter() - start) * 1000
        try:
            people = db.fetch_all("select distinct on (role) user_id, role::text as role from users where active_status order by role, user_id")
            semester = db.fetch_one("select semester_id from semesters order by start_date desc limit 1") or {}
            period = db.fetch_one("select period_id from registration_periods order by start_date desc limit 1") or {}
            major = db.fetch_one("select major_code from majors order by major_code limit 1") or {}
        finally:
            db.close()
        admin = Administrator()
        operations = {
            "admin.dashboard": admin.dashboard, "admin.users": admin.list_users,
            "admin.majors": admin.manageMajor, "admin.courses": admin.manageCourse,
            "admin.semesters": admin.manageSemester, "admin.periods": admin.manageRegistrationPeriod,
            "admin.curriculum": lambda: admin.manageCurriculum(major.get("major_code")),
            "admin.demand": lambda: admin.generateRegistrationDemandReport(period),
            "admin.assignments": lambda: admin.list_assignments(semester),
        }
        for identity in people:
            if identity["role"] == "student":
                student = Student(identity)
                operations.update({
                    "student.profile": student.viewProfile,
                    "student.semesters": student.viewSemesters,
                    "student.periods": student.viewRegistrationPeriods,
                    "student.curriculum": student.viewCurriculum,
                    "student.courses": lambda: student.viewCourses(period),
                    "student.registrations": lambda: student.viewRegistrationStatus(semester),
                    "student.grades": lambda: student.viewGrades(semester),
                })
            if identity["role"] == "lecturer":
                lecturer = Lecturer(identity)
                operations.update({
                    "lecturer.profile": lecturer.viewProfile,
                    "lecturer.semesters": lecturer.viewSemesters,
                    "lecturer.courses": lambda: lecturer.viewTeachingCourse(semester),
                })
                assigned = lecturer.viewTeachingCourse(semester)
                if isinstance(assigned, list) and assigned:
                    code = assigned[0]["course_code"]
                    operations["lecturer.students"] = lambda: lecturer.viewRegisteredStudents(code, semester)
        if people:
            identity = people[0]
            operations["account.me"] = User(identity).viewAccountInfo

            def auth_status():
                db = database.get_db()
                try:
                    return db.fetch_one("select active_status from users where user_id=%s", (identity["user_id"],))
                finally:
                    db.close()
            operations["auth-status-only"] = auth_status
        operations["health-http-test-client"] = lambda: app.test_client().get("/api/health").get_json()
        metrics = {}

        def timed(name, original):
            def call(*args, **kwargs):
                start = perf_counter()
                try:
                    return original(*args, **kwargs)
                finally:
                    metrics[name] = metrics.get(name, 0) + (perf_counter() - start) * 1000
                    if name == "sql_ms":
                        metrics["queries"] = metrics.get("queries", 0) + 1
            return call

        from contextlib import ExitStack
        results = {"cold_acquire_and_timezone_ms": round(cold_ms, 2), "samples": 3, "operations": {}}
        with ExitStack() as stack:
            for method, metric in (("__init__", "acquire_timezone_ms"), ("fetch_one", "sql_ms"),
                                   ("fetch_all", "sql_ms"), ("close", "cleanup_ms")):
                stack.enter_context(patch.object(database.Database, method, timed(metric, getattr(database.Database, method))))
            for name, operation in operations.items():
                samples = []
                for _ in range(3):
                    metrics.clear()
                    start = perf_counter()
                    value = operation()
                    elapsed = (perf_counter() - start) * 1000
                    serialize_start = perf_counter()
                    app.json.dumps(value)
                    row = dict(metrics)
                    row["total_model_ms"] = elapsed
                    row["serialize_ms"] = (perf_counter() - serialize_start) * 1000
                    row["python_ms"] = max(0, elapsed - sum(metrics.get(k, 0) for k in ("sql_ms", "acquire_timezone_ms", "cleanup_ms")))
                    samples.append(row)
                results["operations"][name] = {key: round(statistics.median(row.get(key, 0) for row in samples), 2) for key in samples[0]}
                print(name, results["operations"][name], flush=True)
        Path(sys.argv[1]).write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Driver exceptions can contain host/user names. Do not print them.
        print("Read-only benchmark failed:", type(error).__name__)
        sys.exit(1)
