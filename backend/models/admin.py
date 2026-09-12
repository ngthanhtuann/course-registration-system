"""Functions for the Administrator role."""

from database import get_db
from .user import User
from uuid import uuid4
from datetime import date
import re
import psycopg2
from utils.password import hash_password
from .semester import Semester
from .teaching_assignment import TeachingAssignment
from .course import Course


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _required_text(value, field_name):
    """Return a trimmed non-empty string or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    return value


def _optional_text(value, field_name):
    """Validate an optional string."""
    if value is None:
        return None
    return _required_text(value, field_name)


def _valid_email(value):
    """Validate and normalize an email address."""
    email = _required_text(value, "Email")
    if not _EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email address")
    return email


def _text_list(value, field_name):
    """Validate a list of non-empty strings and remove duplicates."""
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    cleaned = []
    for item in value:
        text = _required_text(item, f"{field_name} item")
        if text not in cleaned:
            cleaned.append(text)
    return cleaned


def _positive_integer(value, field_name):
    """Validate a positive integer."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(f"{field_name} must be a positive integer")
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a positive integer") from exc
    if number <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return number


def _parse_iso_date(value, field_name):
    """Parse an exact YYYY-MM-DD date string."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")

    value = value.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format")

    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid date")


class Administrator(User):
    """Administrator functions for managing the course registration system."""

    def __init__(self, identity=None):
        """Create an Administrator object from user information."""
        super().__init__(identity)

    def dashboard(self):
        """Get information for the admin dashboard."""

        db = get_db()

        try:

            row = db.fetch_one(
                """
                with current_semester as (
                    select
                        semester_id,
                        semester_name,
                        start_date,
                        end_date

                    from semesters

                    where current_date
                          between start_date
                          and end_date

                    order by start_date desc

                    limit 1
                )

                select

                    (
                        select count(*)
                        from students
                    ) as total_students,

                    (
                        select count(*)

                        from lecturers l

                        where exists (
                            select 1

                            from users u

                            where
                                u.user_id = l.user_id
                                and u.active_status = true
                        )
                    ) as active_lecturers,

                    (
                        select count(*)
                        from courses
                    ) as total_courses,

                    (
                        select count(*)

                        from registrations

                        where
                            registration_status = 'registered'
                    ) as active_registrations,

                    cs.semester_id,
                    cs.semester_name,
                    cs.start_date,
                    cs.end_date

                from (
                    select 1
                ) base

                left join current_semester cs
                    on true
                """
            )

            if not row:

                return {
                    "total_students": 0,
                    "active_lecturers": 0,
                    "total_courses": 0,
                    "active_registrations": 0,
                    "active_semester": None,
                }

            active_semester = None

            if row.get("semester_id"):

                active_semester = {
                    "semester_id":
                        row.get("semester_id"),

                    "semester_name":
                        row.get("semester_name"),

                    "start_date":
                        row.get("start_date"),

                    "end_date":
                        row.get("end_date"),
                }

            return {
                "total_students":
                    row.get(
                        "total_students",
                        0
                    ),

                "active_lecturers":
                    row.get(
                        "active_lecturers",
                        0
                    ),

                "total_courses":
                    row.get(
                        "total_courses",
                        0
                    ),

                "active_registrations":
                    row.get(
                        "active_registrations",
                        0
                    ),

                "active_semester":
                    active_semester,
            }

        finally:

            db.close()

    def list_users(self):
        """Get all users."""
        db = get_db()
        try:
            users = db.fetch_all("""
                select u.user_id, u.username, u.full_name as fullname, u.email,
                       lower(u.role::text) as role, u.active_status as status,
                       s.student_id, s.major_code, l.lecturer_id,
                       coalesce(array_agg(distinct q.course_code)
                           filter (where q.course_code is not null), '{}') as qualifications
                from users u
                left join students s on s.user_id=u.user_id
                left join lecturers l on l.user_id=u.user_id
                left join lecturer_qualifications q on q.lecturer_id=l.lecturer_id
                group by u.user_id,s.student_id,l.lecturer_id
                order by u.role,u.user_id
            """)
            return users
        finally:
            db.close()

    def create_user(self, data):
        """Create a new student or lecturer account."""
        data = data or {}

        try:
            user_id = _required_text(data.get("user_id"), "User ID")
            fullname = _required_text(data.get("fullname"), "Full name")
            email = _valid_email(data.get("email"))

            password = data.get("password")
            if not isinstance(password, str):
                raise ValueError("Password must be a string")
            if not password:
                raise ValueError("Password is required")
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters")

            role = _required_text(data.get("role"), "Role").lower()
            if role not in ("lecturer", "student"):
                raise ValueError("Admin can only create lecturer or student")

            major_code = _optional_text(data.get("major_code"), "Major code")
            dob = data.get("dob")
            if dob in (None, ""):
                dob = None
            else:
                dob = _parse_iso_date(dob, "Date of birth").isoformat()

            qualifications = data.get("qualifications")
            if qualifications is None:
                qualifications = []
            qualifications = _text_list(qualifications, "Qualifications")

            if role == "student" and not major_code:
                raise ValueError("Major is required for student")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        username = user_id.lower()
        db = get_db()
        try:
            if role == "student":
                major = db.fetch_one(
                    "select major_code from majors where major_code=%s",
                    (major_code,),
                )
                if not major:
                    return ({"error": "Major does not exist"}, 400)

            old_user = db.fetch_one(
                """
                select user_id
                from users
                where user_id = %s
                   or username = %s
                   or email = %s
                """,
                (user_id, username, email),
            )
            if old_user:
                return ({"error": "User ID, username or email already exists"}, 409)

            if role == "lecturer":
                for course_code in qualifications:
                    if not db.fetch_one(
                        "select course_code from courses where course_code=%s",
                        (course_code,),
                    ):
                        return ({"error": f"Course does not exist: {course_code}"}, 400)

            password_hash = hash_password(password)

            db.execute(
                """
                insert into users
                (user_id, username, password_hash, full_name, email, role)
                values (%s, %s, %s, %s, %s, %s)
                """,
                (user_id, username, password_hash, fullname, email, role),
            )

            if role == "lecturer":
                db.execute(
                    """
                    insert into lecturers
                    (lecturer_id, user_id)
                    values (%s, %s)
                    """,
                    (user_id, user_id),
                )

                for course_code in qualifications:
                    db.execute(
                        """
                        insert into lecturer_qualifications
                        (qualification_id, lecturer_id, course_id, course_code)
                        values (%s, %s, (select course_id from courses where course_code=%s), %s)
                        """,
                        (uuid4().hex[:20], user_id, course_code, course_code),
                    )

            if role == "student":
                db.execute(
                    """
                    insert into students
                    (student_id, user_id, date_of_birth, major_id, major_code)
                    values (%s, %s, %s,
                            (select major_id from majors where major_code=%s), %s)
                    """,
                    (user_id, user_id, dob, major_code, major_code),
                )

            db.conn.commit()
            return (
                {
                    "message": "User created successfully",
                    "user_id": user_id,
                    "username": username,
                    "role": role,
                },
                201,
            )
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "User data conflicts with an existing record"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_user(self, user_id, data):
        """Update user information."""
        data = data or {}

        fullname = data.get("fullname")
        email = data.get("email")
        major_code = data.get("major_code")
        status = data.get("status")
        qualifications = data.get("qualifications", None)

        if (
            fullname is None
            and email is None
            and major_code is None
            and status is None
            and qualifications is None
        ):
            return ({"error": "Nothing to update"}, 400)

        try:
            if fullname is not None:
                fullname = _required_text(fullname, "Full name")
            if email is not None:
                email = _valid_email(email)
            if major_code is not None:
                major_code = _required_text(major_code, "Major code")
            if status is not None:
                status = _required_text(status, "Status").lower()
                if status not in ("active", "inactive"):
                    raise ValueError("Invalid status")
            if qualifications is not None:
                qualifications = _text_list(qualifications, "Qualifications")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            user = db.fetch_one(
                "select user_id, lower(role::text) as role from users where user_id=%s",
                (user_id,),
            )
            if not user:
                return ({"error": "User not found"}, 404)

            if email is not None:
                duplicate = db.fetch_one(
                    "select user_id from users where email=%s and user_id<>%s",
                    (email, user_id),
                )
                if duplicate:
                    return ({"error": "Email already exists"}, 409)

            if major_code is not None:
                if user["role"] != "student":
                    return ({"error": "Major can only be changed for students"}, 400)
                if not db.fetch_one(
                    "select major_code from majors where major_code=%s",
                    (major_code,),
                ):
                    return ({"error": "Major does not exist"}, 400)

            if qualifications is not None:
                if user["role"] != "lecturer":
                    return ({"error": "Qualifications can only be changed for lecturers"}, 400)

                for course_code in qualifications:
                    if not db.fetch_one(
                        "select course_code from courses where course_code=%s",
                        (course_code,),
                    ):
                        return ({"error": f"Course does not exist: {course_code}"}, 400)

            db.execute(
                """
                update users
                set full_name=coalesce(%s,full_name),
                    email=coalesce(%s,email),
                    active_status=coalesce(%s,active_status)
                where user_id=%s
                """,
                (
                    fullname,
                    email,
                    status == "active" if status is not None else None,
                    user_id,
                ),
            )

            if major_code is not None:
                db.execute(
                    """
                    update students
                    set major_code=%s,
                        major_id=(select major_id from majors where major_code=%s)
                    where user_id=%s
                    """,
                    (major_code, major_code, user_id),
                )

            if qualifications is not None:
                db.execute(
                    """
                    delete from lecturer_qualifications
                    where lecturer_id=(select lecturer_id from lecturers where user_id=%s)
                    """,
                    (user_id,),
                )

                for course_code in qualifications:
                    db.execute(
                        """
                        insert into lecturer_qualifications
                        (qualification_id, lecturer_id, course_id, course_code)
                        values (%s, (select lecturer_id from lecturers where user_id=%s),
                                (select course_id from courses where course_code=%s), %s)
                        """,
                        (uuid4().hex[:20], user_id, course_code, course_code),
                    )

            db.conn.commit()
            return {"message": "User updated successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "User data conflicts with an existing record"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def deactivate_user(self, user_id):
        """Deactivate a user account."""
        db = get_db()
        try:
            row = db.fetch_one(
                "select lower(role::text) as role from users where user_id=%s", (user_id,)
            )
            if not row:
                return ({"error": "User not found"}, 404)
            if row["role"] == "admin":
                return ({"error": "Administrator cannot be deactivated"}, 400)
            db.execute(
                "update users set active_status=false where user_id=%s", (user_id,)
            )
            db.conn.commit()
            return {"message": "User deactivated successfully"}
        finally:
            db.close()

    def manageMajor(self):
        """Get all majors."""
        db = get_db()
        try:
            majors = db.fetch_all("""
            select major_code, major_name
            from majors
            order by major_code
        """)
            return majors
        finally:
            db.close()

    def create_major(self, data):
        """Create a new major."""
        data = data or {}
        try:
            major_code = _required_text(data.get("major_code"), "Major code")
            major_name = _required_text(data.get("major_name"), "Major name")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            db.execute_query(
                """
                insert into majors
                (major_code, major_name)
                values (%s, %s)
                """,
                (major_code, major_name),
            )
            return ({"message": "Major created successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Major code already exists or data conflicts with existing records"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_major(self, major_code, data):
        """Update a major."""
        data = data or {}
        try:
            major_name = _required_text(data.get("major_name"), "Major name")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            affected = db.execute_query(
                """
                update majors
                set major_name = %s
                where major_code = %s
                """,
                (major_name, major_code),
            )
            if affected == 0:
                return ({"error": "Major not found"}, 404)
            return {"message": "Major updated successfully"}
        finally:
            db.close()

    def delete_major(self, major_code):
        """Delete a major."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
                delete from majors
                where major_code = %s
                """,
                (major_code,),
            )
            if affected == 0:
                return ({"error": "Major not found"}, 404)
            return {"message": "Major deleted successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Major is still referenced by existing data"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def manageCourse(self):
        """Get all courses."""
        db = get_db()
        try:
            courses = db.fetch_all("""
            select
                c.course_code,
                c.course_name,
                c.credit,
                c.prerequisite_course_code,
                p.course_name as prerequisite_name,
                c.max_capacity
            from courses c
            left join courses p
                on p.course_code = c.prerequisite_course_code
            order by c.course_code
        """)
            return courses
        finally:
            db.close()

    def create_course(self, data):
        """Create a new course."""
        data = data or {}
        try:
            course_code = _required_text(data.get("course_code"), "Course code")
            course_name = _required_text(data.get("course_name"), "Course name")
            prerequisite = _optional_text(
                data.get("prerequisite_course_code"),
                "Prerequisite course code",
            )
            credit = Course.positiveInteger(data.get("credit"))
            max_capacity = Course.positiveInteger(data.get("max_capacity"))
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if prerequisite == course_code:
            return ({"error": "A course cannot be its own prerequisite"}, 400)

        db = get_db()
        try:
            db.execute_query(
                """
                insert into courses
                (course_code, course_name, credit, prerequisite_course_code, max_capacity)
                values (%s, %s, %s, %s, %s)
                """,
                (course_code, course_name, credit, prerequisite, max_capacity),
            )
            return ({"message": "Course created successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Invalid prerequisite or duplicate course code"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_course(self, course_code, data):
        """Update a course."""
        data = data or {}

        try:
            prerequisite = _optional_text(
                data.get("prerequisite_course_code"),
                "Prerequisite course code",
            )
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if prerequisite == course_code:
            return ({"error": "A course cannot be its own prerequisite"}, 400)

        db = get_db()
        try:
            current = db.fetch_one(
                "select course_name, credit, max_capacity, prerequisite_course_code from courses where course_code=%s for update",
                (course_code,),
            )
            if not current:
                return ({"error": "Course not found"}, 404)

            try:
                course_name = _required_text(
                    data.get("course_name", current["course_name"]),
                    "Course name",
                )
                credit = Course.positiveInteger(data.get("credit", current["credit"]))
                max_capacity = Course.positiveInteger(
                    data.get("max_capacity", current["max_capacity"])
                )
            except ValueError as exc:
                return ({"error": str(exc)}, 400)

            if "prerequisite_course_code" not in data:
                prerequisite = current["prerequisite_course_code"]

            db.execute_query(
                """
                update courses
                set course_name=%s,
                    credit=%s,
                    prerequisite_course_code=%s,
                    max_capacity=%s
                where course_code=%s
                """,
                (course_name, credit, prerequisite, max_capacity, course_code),
            )
            return {"message": "Course updated successfully"}
        except (psycopg2.IntegrityError, psycopg2.errors.RaiseException):
            db.conn.rollback()
            return ({"error": "Invalid prerequisite or capacity below registered student count"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def delete_course(self, course_code):
        """Delete a course."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
                delete from courses
                where course_code = %s
                """,
                (course_code,),
            )
            if affected == 0:
                return ({"error": "Course not found"}, 404)
            return {"message": "Course deleted successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Course is still referenced by existing data"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def manageCurriculum(self, major_code):
        """Get the curriculum of a major."""
        db = get_db()
        try:
            curriculum = db.fetch_all(
                """
            select
                cu.curriculum_id,
                cu.major_code,
                cu.course_code,
                c.course_name,
                c.credit,
                c.prerequisite_course_code,
                cu.recommended_semester
            from curriculum cu
            join courses c
                on c.course_code = cu.course_code
            where cu.major_code = %s
            order by cu.recommended_semester, cu.course_code
        """,
                (major_code,),
            )
            return curriculum
        finally:
            db.close()

    def add_curriculum(self, data):
        """Add a course to a curriculum."""
        data = data or {}
        try:
            curriculum_id = _optional_text(data.get("curriculum_id"), "Curriculum ID") or uuid4().hex[:20]
            major_code = _required_text(data.get("major_code"), "Major code")
            course_code = _required_text(data.get("course_code"), "Course code")
            semester = data.get("recommended_semester")
            if semester is not None:
                semester = _positive_integer(semester, "Recommended semester")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            db.execute_query(
                """
                insert into curriculum
                (curriculum_id, major_id, course_id, major_code, course_code, recommended_semester)
                values (%s, (select major_id from majors where major_code=%s),
                        (select course_id from courses where course_code=%s), %s, %s, %s)
                """,
                (curriculum_id, major_code, course_code, major_code, course_code, semester),
            )
            return ({"message": "Course added to curriculum"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Course already exists in this major or referenced data is invalid"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_curriculum(self, curriculum_id, data):
        """Update a curriculum item."""
        data = data or {}
        try:
            semester = _positive_integer(
                data.get("recommended_semester"),
                "Recommended semester",
            )
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            affected = db.execute_query(
                """
                update curriculum
                set recommended_semester = %s
                where curriculum_id = %s
                """,
                (semester, curriculum_id),
            )
            if affected == 0:
                return ({"error": "Curriculum item not found"}, 404)
            return {"message": "Curriculum updated successfully"}
        finally:
            db.close()

    def remove_curriculum(self, curriculum_id):
        """Remove a course from a curriculum."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
            delete from curriculum
            where curriculum_id = %s
        """,
                (curriculum_id,),
            )
            if affected == 0:
                return ({"error": "Curriculum item not found"}, 404)
            return {"message": "Course removed from curriculum"}
        finally:
            db.close()

    def manageSemester(self):
        """Get all semesters."""
        db = get_db()
        try:
            semesters = db.fetch_all("""
            select semester_id, semester_name, start_date, end_date,
                   case when current_date < start_date then 'upcoming'
                        when current_date <= end_date then 'active'
                        else 'completed' end as status
            from semesters
            order by start_date desc
        """)
            return semesters
        finally:
            db.close()

    def create_semester(self, data):
        """Create a new semester."""
        data = data or {}
        try:
            semester_id = _optional_text(data.get("semester_id"), "Semester ID") or uuid4().hex[:20]
            semester_name = _required_text(data.get("semester_name"), "Semester name")
            start_date = _parse_iso_date(data.get("start_date"), "Start date").isoformat()
            end_date = _parse_iso_date(data.get("end_date"), "End date").isoformat()
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)

        db = get_db()
        try:
            overlap = Semester(
                semester_name,
                date.fromisoformat(start_date),
                date.fromisoformat(end_date),
                semesterId=None,
            ).overlapsExisting(db)
            if overlap:
                return ({"error": "Semester overlaps an existing semester"}, 409)

            db.execute_query(
                """
                insert into semesters
                (semester_id, semester_name, start_date, end_date, status)
                values (%s, %s, %s, %s, %s)
                """,
                (semester_id, semester_name, start_date, end_date, "PLANNED"),
            )
            return ({"message": "Semester created successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Semester data conflicts with an existing record"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_semester(self, semester_id, data):
        """Update a semester."""
        data = data or {}
        try:
            start_date = _parse_iso_date(data.get("start_date"), "Start date").isoformat()
            end_date = _parse_iso_date(data.get("end_date"), "End date").isoformat()
            semester_name = _required_text(data.get("semester_name"), "Semester name")
            status = _required_text(data.get("status", "PLANNED"), "Status").upper()
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)

        db = get_db()
        try:
            current = db.fetch_one(
                "select semester_id from semesters where semester_id=%s",
                (semester_id,),
            )
            if not current:
                return ({"error": "Semester not found"}, 404)

            overlap = Semester(
                semester_name,
                date.fromisoformat(start_date),
                date.fromisoformat(end_date),
                semesterId=semester_id,
            ).overlapsExisting(db)
            if overlap:
                return ({"error": "Semester overlaps an existing semester"}, 409)

            affected = db.execute_query(
                """
                update semesters
                set semester_name = %s,
                    start_date = %s,
                    end_date = %s,
                    status = %s
                where semester_id = %s
                """,
                (semester_name, start_date, end_date, status, semester_id),
            )
            if affected == 0:
                return ({"error": "Semester not found"}, 404)
            return {"message": "Semester updated successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Semester data conflicts with existing records"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def delete_semester(self, semester_id):
        """Delete a semester."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
                delete from semesters
                where semester_id = %s
                """,
                (semester_id,),
            )
            if affected == 0:
                return ({"error": "Semester not found"}, 404)
            return {"message": "Semester deleted successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Semester is still referenced"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def manageRegistrationPeriod(self):
        """Get all registration periods."""
        db = get_db()
        try:
            periods = db.fetch_all("""
            select
                rp.*,
                s.semester_name,
                case
                    when current_date < rp.start_date
                        then 'upcoming'
                    when current_date <= rp.end_date
                        then 'open'
                    else 'closed'
                end as current_status,
                case
                    when current_date < rp.drop_start_date then 'upcoming'
                    when current_date <= rp.drop_end_date then 'open'
                    else 'closed'
                end as current_drop_status
            from registration_periods rp
            join semesters s
                on s.semester_id = rp.semester_id
            order by rp.start_date desc
        """)
            return periods
        finally:
            db.close()

    def create_period(self, data):
        """Create a new registration period."""
        data = data or {}
        try:
            semester_id = _required_text(data.get("semester_id"), "Semester ID")
            period_id = _optional_text(data.get("period_id"), "Period ID") or uuid4().hex[:20]
            period_name = _optional_text(data.get("period_name"), "Period name") or "Registration Period"
            start_date = _parse_iso_date(data.get("start_date"), "Start date").isoformat()
            end_date = _parse_iso_date(data.get("end_date"), "End date").isoformat()
            drop_start_date = _parse_iso_date(data.get("drop_start_date"), "Drop start date").isoformat()
            drop_end_date = _parse_iso_date(data.get("drop_end_date"), "Drop end date").isoformat()
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        if drop_start_date >= drop_end_date:
            return ({"error": "Drop start date must be earlier than drop end date"}, 400)

        db = get_db()
        try:
            semester = db.fetch_one(
                "select start_date, end_date from semesters where semester_id = %s",
                (semester_id,),
            )
            if not semester:
                return ({"error": "Semester not found"}, 404)

            if start_date < str(semester["start_date"]) or end_date > str(semester["end_date"]):
                return ({"error": "Registration period must fall within the semester"}, 400)
            if drop_start_date < str(semester["start_date"]) or drop_end_date > str(semester["end_date"]):
                return ({"error": "Drop period must fall within the semester"}, 400)

            db.execute_query(
                """
                insert into registration_periods
                (period_id, semester_id, period_name, start_date, end_date, drop_start_date, drop_end_date)
                values (%s, %s, %s, %s, %s, %s, %s)
                """,
                (period_id, semester_id, period_name, start_date, end_date, drop_start_date, drop_end_date),
            )
            return ({"message": "Registration period created successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Registration period conflicts with existing data"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def update_period(self, period_id, data):
        """Update a registration period."""
        data = data or {}
        try:
            semester_id = _required_text(data.get("semester_id"), "Semester ID")
            period_name = _optional_text(data.get("period_name"), "Period name") or "Registration Period"
            start_date = _parse_iso_date(data.get("start_date"), "Start date").isoformat()
            end_date = _parse_iso_date(data.get("end_date"), "End date").isoformat()
            drop_start_date = _parse_iso_date(data.get("drop_start_date"), "Drop start date").isoformat()
            drop_end_date = _parse_iso_date(data.get("drop_end_date"), "Drop end date").isoformat()
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        if drop_start_date >= drop_end_date:
            return ({"error": "Drop start date must be earlier than drop end date"}, 400)

        db = get_db()
        try:
            current = db.fetch_one(
                "select period_id, semester_id from registration_periods where period_id=%s for update",
                (period_id,),
            )
            if not current:
                return ({"error": "Registration period not found"}, 404)
            if current["semester_id"] != semester_id and db.fetch_one(
                "select 1 from registrations where period_id=%s limit 1", (period_id,)
            ):
                return ({"error": "A period with registrations cannot move to another semester"}, 409)

            semester = db.fetch_one(
                "select start_date, end_date from semesters where semester_id = %s",
                (semester_id,),
            )
            if not semester:
                return ({"error": "Semester not found"}, 404)

            if start_date < str(semester["start_date"]) or end_date > str(semester["end_date"]):
                return ({"error": "Registration period must fall within the semester"}, 400)
            if drop_start_date < str(semester["start_date"]) or drop_end_date > str(semester["end_date"]):
                return ({"error": "Drop period must fall within the semester"}, 400)

            affected = db.execute_query(
                """
                update registration_periods
                set semester_id = %s,
                    period_name = %s,
                    start_date = %s,
                    end_date = %s,
                    drop_start_date = %s,
                    drop_end_date = %s
                where period_id = %s
                """,
                (semester_id, period_name, start_date, end_date, drop_start_date, drop_end_date, period_id),
            )
            if affected == 0:
                return ({"error": "Registration period not found"}, 404)
            return {"message": "Registration period updated successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Registration period conflicts with existing data"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def delete_period(self, period_id):
        """Delete a registration period."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
                delete from registration_periods
                where period_id = %s
                """,
                (period_id,),
            )
            if affected == 0:
                return ({"error": "Registration period not found"}, 404)
            return {"message": "Registration period deleted successfully"}
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Registration period is still referenced"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def generateRegistrationDemandReport(self, query):
        """Get registration demand for courses."""
        period_id = query.get("period_id")
        major_code = query.get("major_code") or None
        search = query.get("search", "").strip()
        if not period_id:
            return ({"error": "period_id is required"}, 400)
        db = get_db()
        try:
            if not db.fetch_one(
                "select period_id from registration_periods where period_id=%s", (period_id,)
            ):
                return ({"error": "Registration period not found"}, 404)
            if major_code and not db.fetch_one(
                "select major_code from majors where major_code=%s", (major_code,)
            ):
                return ({"error": "Major not found"}, 404)
            demand = db.fetch_all(
                """
            select
                c.course_code,
                c.course_name,
                c.credit,
                c.max_capacity,
                count(distinct r.registration_id)
                filter (
                    where r.registration_status = 'registered'
                      and (%s is null or s.major_code = %s)
                ) as registered_students
            from curriculum cu
            join courses c
                on c.course_code = cu.course_code
            left join registrations r
                on r.course_code = c.course_code
               and r.period_id = %s
            left join students s
                on s.student_id = r.student_id
            where (%s is null or cu.major_code = %s)
              and (c.course_code ilike %s or c.course_name ilike %s)
            group by c.course_code, c.course_name, c.credit, c.max_capacity
            order by c.course_code
        """,
                (major_code, major_code, period_id, major_code, major_code, f"%{search}%", f"%{search}%"),
            )
            return demand
        finally:
            db.close()

    def demand_students(self, course_code, query):
        """Get students registered for a course in a period."""
        period_id = query.get("period_id")
        major_code = query.get("major_code") or None
        if not period_id:
            return ({"error": "period_id is required"}, 400)
        db = get_db()
        try:
            if not db.fetch_one(
                "select period_id from registration_periods where period_id=%s", (period_id,)
            ):
                return ({"error": "Registration period not found"}, 404)
            if not db.fetch_one(
                "select 1 from courses c where c.course_code=%s and "
                "(%s is null or exists (select 1 from curriculum cu "
                "where cu.course_code=c.course_code and cu.major_code=%s))",
                (course_code, major_code, major_code),
            ):
                return ({"error": "Course not found in the selected curriculum"}, 404)
            students = db.fetch_all(
                """
            select
                s.student_id,
                u.full_name as fullname,
                u.email,
                r.registration_status
            from registrations r
            join students s
                on s.student_id = r.student_id
            join users u
                on u.user_id = s.user_id
            where r.period_id = %s
              and r.course_code = %s
              and r.registration_status = 'registered'
              and (%s is null or s.major_code = %s)
            order by s.student_id
        """,
                (period_id, course_code, major_code, major_code),
            )
            return students
        finally:
            db.close()

    def list_assignments(self, query):
        """Get teaching assignments."""
        semester_id = query.get("semester_id")
        db = get_db()
        try:
            assignments = db.fetch_all(
                """
            select
                ta.assignment_id,
                ta.semester_id,
                ta.lecturer_id,
                ta.course_code,
                u.full_name as lecturer_name,
                c.course_name,
                s.semester_name
            from teaching_assignments ta
            join lecturers l
                on l.lecturer_id = ta.lecturer_id
            join users u
                on u.user_id = l.user_id
            join courses c
                on c.course_code = ta.course_code
            join semesters s
                on s.semester_id = ta.semester_id
            where (%s is null or ta.semester_id = %s)
            order by s.start_date desc, c.course_code
        """,
                (semester_id, semester_id),
            )
            return assignments
        finally:
            db.close()

    def delete_assignment(self, assignment_id):
        """Delete a teaching assignment."""
        db = get_db()
        try:
            affected = db.execute_query(
                """
            delete from teaching_assignments
            where assignment_id = %s
        """,
                (assignment_id,),
            )
            if affected == 0:
                return ({"error": "Teaching assignment not found"}, 404)
            return {"message": "Teaching assignment deleted successfully"}
        finally:
            db.close()

    def qualified_lecturers(self, course_code):
        """Get lecturers who are qualified to teach a course."""
        db = get_db()
        try:
            lecturers = db.fetch_all(
                """
            select
                l.lecturer_id,
                u.full_name as fullname,
                u.email
            from lecturer_qualifications q
            join lecturers l
                on l.lecturer_id = q.lecturer_id
            join users u
                on u.user_id = l.user_id
            where q.course_code = %s
              and exists (select 1 from users au where au.user_id=l.user_id and au.active_status=true)
            order by l.lecturer_id
        """,
                (course_code,),
            )
            return lecturers
        finally:
            db.close()

    def add_qualification(self, data):
        """Add a qualification to a lecturer."""
        data = data or {}
        try:
            qualification_id = _optional_text(data.get("qualification_id"), "Qualification ID") or uuid4().hex[:20]
            lecturer_id = _required_text(data.get("lecturer_id"), "Lecturer ID")
            course_code = _required_text(data.get("course_code"), "Course code")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            db.execute_query(
                """
                insert into lecturer_qualifications
                (qualification_id, lecturer_id, course_id, course_code)
                values (%s, %s, (select course_id from courses where course_code=%s), %s)
                """,
                (qualification_id, lecturer_id, course_code, course_code),
            )
            return ({"message": "Qualification added successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Invalid or duplicate qualification"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def remove_qualification(self, lecturer_id, course_code):
        """Remove a qualification from a lecturer."""
        db = get_db()
        try:
            row = db.fetch_one(
                """
            select qualification_id
            from lecturer_qualifications
            where lecturer_id=%s and course_code=%s
        """,
                (lecturer_id, course_code),
            )
            if not row:
                return ({"error": "Qualification not found"}, 404)
            db.execute_query(
                "delete from lecturer_qualifications where lecturer_id=%s and course_code=%s",
                (lecturer_id, course_code),
            )
            return {"message": "Qualification removed successfully"}
        finally:
            db.close()

    def assignLecturer(self, data):
        """Assign a qualified lecturer to a course."""
        data = data or {}
        try:
            assignment_id = _optional_text(data.get("assignment_id"), "Assignment ID") or uuid4().hex[:20]
            semester_id = _required_text(data.get("semester_id"), "Semester ID")
            lecturer_id = _required_text(data.get("lecturer_id"), "Lecturer ID")
            course_code = _required_text(data.get("course_code"), "Course code")
            major_code = _required_text(data.get("major_code"), "Major code")
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        db = get_db()
        try:
            if not db.fetch_one(
                "select curriculum_id from curriculum where major_code=%s and course_code=%s for share",
                (major_code, course_code),
            ):
                return ({"error": "Course does not belong to the selected major's curriculum"}, 400)
            assignment = TeachingAssignment(
                assignment_id,
                lecturer_id,
                course_code,
                semester_id,
            )
            if not assignment.isQualified(db):
                return ({"error": "Lecturer is not qualified for this course"}, 400)

            assignment.save(db)
            return ({"message": "Lecturer assigned successfully"}, 201)
        except psycopg2.IntegrityError:
            db.conn.rollback()
            return ({"error": "Invalid assignment or duplicate assignment"}, 409)
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def manageStudent(self):
        """Get all student accounts."""
        students = []
        for user in self.list_users():
            if user["role"] == "student":
                students.append(user)
        return students

    def manageLecturer(self):
        """Get all lecturer accounts."""
        lecturers = []
        for user in self.list_users():
            if user["role"] == "lecturer":
                lecturers.append(user)
        return lecturers
