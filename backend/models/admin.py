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


class Administrator(User):
    """Administrator functions for managing the course registration system."""

    def __init__(self, identity=None):
        """Create an Administrator object from user information."""
        super().__init__(identity)

    def dashboard(self):
        """Get information for the admin dashboard."""
        db = get_db()
        try:
            # Read counts and the current semester in one trip to remote Neon.
            counts = db.fetch_one("""
            select counts.*, semester.semester_id, semester.semester_name,
                   semester.start_date, semester.end_date
            from (select
                (select count(*) from students) as total_students,
                (select count(*) from lecturers where exists (
                    select 1 from users u where u.user_id=lecturers.user_id and u.active_status=true
                )) as active_lecturers,
                (select count(*) from courses) as total_courses,
                (select count(*) from registrations where registration_status='registered') as active_registrations
            ) counts
            left join (
                select semester_id, semester_name, start_date, end_date
                from semesters
                where current_date between start_date and end_date
                order by start_date desc
                limit 1
            ) semester on true
        """)
            semester = {key: counts.pop(key) for key in (
                "semester_id", "semester_name", "start_date", "end_date"
            )}
            if semester["semester_id"] is None:
                semester = None
            return {**(counts or {}), "active_semester": semester}
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
        user_id = data.get("user_id")
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        if not user_id or not fullname or (not email) or (not password) or (not role):
            return ({"error": "Missing required information"}, 400)
        if not re.match("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$", str(email).strip()):
            return ({"error": "Invalid email address"}, 400)
        if len(str(password)) < 8:
            return ({"error": "Password must be at least 8 characters"}, 400)
        if role not in ["lecturer", "student"]:
            return ({"error": "Admin can only create lecturer or student"}, 400)
        username = user_id.lower()
        db = get_db()
        try:
            major_code = data.get("major_code")
            dob = data.get("dob")
            if role == "student":
                if not major_code:
                    return ({"error": "Major is required for student"}, 400)
                major = db.fetch_one(
                    "select major_code from majors where major_code=%s", (major_code,)
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
            password_hash = hash_password(password)
            db.execute(
                """
            insert into users
            (user_id, username, password_hash, full_name, email, role)
            values (%s, %s, %s, %s, %s, %s)
        """,
                (
                    user_id,
                    username,
                    password_hash,
                    fullname,
                    email,
                    role,
                ),
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
                qualifications = data.get("qualifications") or []
                if not isinstance(qualifications, list):
                    raise ValueError("qualifications must be a list")
                for course_code in dict.fromkeys(
                    (str(x).strip() for x in qualifications if str(x).strip())
                ):
                    if not db.fetch_one(
                        "select course_code from courses where course_code=%s",
                        (course_code,),
                    ):
                        raise ValueError(f"Course does not exist: {course_code}")
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
        except Exception:
            db.conn.rollback()
            return ({"error": "Could not create user"}, 400)
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
            and (major_code is None)
            and (status is None)
            and (qualifications is None)
        ):
            return ({"error": "Nothing to update"}, 400)
        db = get_db()
        try:
            user = db.fetch_one(
                "select user_id, lower(role::text) as role from users where user_id=%s", (user_id,)
            )
            if not user:
                return ({"error": "User not found"}, 404)
            if email:
                email = str(email).strip()
                if not re.match("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$", email):
                    return ({"error": "Invalid email address"}, 400)
                dup = db.fetch_one(
                    "select user_id from users where email=%s and user_id<>%s",
                    (email, user_id),
                )
                if dup:
                    return ({"error": "Email already exists"}, 409)
            if status is not None and status not in (
                "Active",
                "Inactive",
                "active",
                "inactive",
            ):
                return ({"error": "Invalid status"}, 400)
            if major_code is not None:
                if user["role"] != "student":
                    return ({"error": "Major can only be changed for students"}, 400)
                if not db.fetch_one(
                    "select major_code from majors where major_code=%s", (major_code,)
                ):
                    return ({"error": "Major does not exist"}, 400)
            if qualifications is not None:
                if user["role"] != "lecturer" or not isinstance(qualifications, list):
                    return (
                        {"error": "Qualifications can only be changed for lecturers"},
                        400,
                    )
                clean_qualifications = list(
                    dict.fromkeys(
                        (str(x).strip() for x in qualifications if str(x).strip())
                    )
                )
                for course_code in clean_qualifications:
                    if not db.fetch_one(
                        "select course_code from courses where course_code=%s",
                        (course_code,),
                    ):
                        return ({"error": f"Course does not exist: {course_code}"}, 400)
            db.execute(
                """update users set full_name=coalesce(%s,full_name), email=coalesce(%s,email),
            active_status=coalesce(%s,active_status) where user_id=%s""",
                (
                    fullname,
                    email,
                    str(status).lower() == "active" if status is not None else None,
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
                for course_code in clean_qualifications:
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
        except Exception:
            db.conn.rollback()
            return ({"error": "Could not update user"}, 400)
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
        major_code = data.get("major_code")
        major_name = data.get("major_name")
        if not major_code or not major_name:
            return ({"error": "Major code and major name are required"}, 400)
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
        except Exception:
            db.conn.rollback()
            return ({"error": "Major code already exists or data is invalid"}, 409)
        finally:
            db.close()

    def update_major(self, major_code, data):
        """Update a major."""
        data = data or {}
        major_name = data.get("major_name")
        if not major_name:
            return ({"error": "Major name is required"}, 400)
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
        except Exception:
            db.conn.rollback()
            return ({"error": "Major is still referenced by existing data"}, 409)
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
        course_code = data.get("course_code")
        course_name = data.get("course_name")
        credit = data.get("credit")
        prerequisite = data.get("prerequisite_course_code")
        max_capacity = data.get("max_capacity")
        if (
            not course_code
            or not course_name
            or credit is None
            or (max_capacity is None)
        ):
            return ({"error": "Missing course information"}, 400)
        try:
            credit = Course.positiveInteger(credit)
            max_capacity = Course.positiveInteger(max_capacity)
        except ValueError as exc:
            return ({"error": str(exc)}, 400)
        if prerequisite == course_code:
            return ({"error": "A course cannot be its own prerequisite"}, 400)
        db = get_db()
        try:
            db.execute_query(
                """
            insert into courses
            (
                course_code,
                course_name,
                credit,
                prerequisite_course_code,
                max_capacity
            )
            values (%s, %s, %s, %s, %s)
        """,
                (
                    course_code,
                    course_name,
                    credit,
                    prerequisite,
                    max_capacity,
                ),
            )
            return ({"message": "Course created successfully"}, 201)
        except Exception:
            db.conn.rollback()
            return ({"error": "Invalid course or duplicate course code"}, 409)
        finally:
            db.close()

    def update_course(self, course_code, data):
        """Update a course."""
        data = data or {}
        prerequisite = data.get("prerequisite_course_code")
        if prerequisite == course_code:
            return ({"error": "A course cannot be its own prerequisite"}, 400)
        db = get_db()
        try:
            current = db.fetch_one(
                "select course_name, credit, max_capacity from courses where course_code=%s for update",
                (course_code,),
            )
            if not current:
                return ({"error": "Course not found"}, 404)
            course_name = data.get("course_name", current["course_name"])
            credit = data.get("credit", current["credit"])
            max_capacity = data.get("max_capacity", current["max_capacity"])
            try:
                credit = Course.positiveInteger(credit)
                max_capacity = Course.positiveInteger(max_capacity)
            except ValueError as exc:
                return ({"error": str(exc)}, 400)
            db.execute_query(
                """
                update courses
                set course_name=%s, credit=%s, prerequisite_course_code=%s,
                    max_capacity=%s
                where course_code=%s
                """,
                (course_name, credit, prerequisite, max_capacity, course_code),
            )
            return {"message": "Course updated successfully"}
        except psycopg2.Error:
            db.conn.rollback()
            return ({"error": "Invalid prerequisite or capacity below registered student count"}, 409)
        finally:
            db.close()

    def delete_course(self, course_code):
        """Delete a course."""
        db = get_db()
        try:
            db.execute_query(
                """
            delete from courses
            where course_code = %s
        """,
                (course_code,),
            )
            return {"message": "Course deleted successfully"}
        except Exception:
            db.conn.rollback()
            return ({"error": "Course is still referenced by existing data"}, 409)
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
        curriculum_id = data.get("curriculum_id") or uuid4().hex[:20]
        major_code = data.get("major_code")
        course_code = data.get("course_code")
        semester = data.get("recommended_semester")
        if not curriculum_id or not major_code or (not course_code):
            return ({"error": "Missing curriculum information"}, 400)
        db = get_db()
        try:
            db.execute_query(
                """
            insert into curriculum
            (
                curriculum_id,
                major_id,
                course_id,
                major_code,
                course_code,
                recommended_semester
            )
            values (%s, (select major_id from majors where major_code=%s),
                    (select course_id from courses where course_code=%s), %s, %s, %s)
        """,
                (curriculum_id, major_code, course_code, major_code, course_code, semester),
            )
            return ({"message": "Course added to curriculum"}, 201)
        except Exception:
            db.conn.rollback()
            return (
                {"error": "Invalid data or course already exists in this major"},
                409,
            )
        finally:
            db.close()

    def update_curriculum(self, curriculum_id, data):
        """Update a curriculum item."""
        data = data or {}
        db = get_db()
        try:
            db.execute_query(
                """
            update curriculum
            set recommended_semester = %s
            where curriculum_id = %s
        """,
                (data.get("recommended_semester"), curriculum_id),
            )
            return {"message": "Curriculum updated successfully"}
        finally:
            db.close()

    def remove_curriculum(self, curriculum_id):
        """Remove a course from a curriculum."""
        db = get_db()
        try:
            db.execute_query(
                """
            delete from curriculum
            where curriculum_id = %s
        """,
                (curriculum_id,),
            )
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
        semester_id = data.get("semester_id") or uuid4().hex[:20]
        semester_name = data.get("semester_name")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not semester_id or not semester_name or (not start_date) or (not end_date):
            return ({"error": "Missing semester information"}, 400)
        try:
            start_date = date.fromisoformat(str(start_date)[:10]).isoformat()
            end_date = date.fromisoformat(str(end_date)[:10]).isoformat()
        except ValueError:
            return ({"error": "Start date and end date must be valid dates"}, 400)
        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        db = get_db()
        try:
            overlap = Semester(
                data.get("semester_name", ""),
                date.fromisoformat(start_date),
                date.fromisoformat(end_date),
                semesterId=None,
            ).overlapsExisting(db)
            if overlap:
                return ({"error": "Semester overlaps an existing semester"}, 409)
            db.execute_query(
                """
            insert into semesters
            (
                semester_id,
                semester_name,
                start_date,
                end_date,
                status
            )
            values (%s, %s, %s, %s, %s)
        """,
                (semester_id, semester_name, start_date, end_date, "PLANNED"),
            )
            return ({"message": "Semester created successfully"}, 201)
        except Exception:
            db.conn.rollback()
            return ({"error": "Invalid semester"}, 409)
        finally:
            db.close()

    def update_semester(self, semester_id, data):
        """Update a semester."""
        data = data or {}
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not start_date or not end_date:
            return ({"error": "Start date and end date are required"}, 400)
        try:
            start_date = date.fromisoformat(str(start_date)[:10]).isoformat()
            end_date = date.fromisoformat(str(end_date)[:10]).isoformat()
        except ValueError:
            return ({"error": "Start date and end date must be valid dates"}, 400)
        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        db = get_db()
        try:
            overlap = Semester(
                data.get("semester_name", ""),
                date.fromisoformat(start_date),
                date.fromisoformat(end_date),
                semesterId=semester_id,
            ).overlapsExisting(db)
            if overlap:
                return ({"error": "Semester overlaps an existing semester"}, 409)
            db.execute_query(
                """
            update semesters
            set semester_name = %s,
                start_date = %s,
                end_date = %s,
                status = %s
            where semester_id = %s
        """,
                (
                    data.get("semester_name"),
                    start_date,
                    end_date,
                    str(data.get("status", "PLANNED")).upper(),
                    semester_id,
                ),
            )
            return {"message": "Semester updated successfully"}
        finally:
            db.close()

    def delete_semester(self, semester_id):
        """Delete a semester."""
        db = get_db()
        try:
            db.execute_query(
                """
            delete from semesters
            where semester_id = %s
        """,
                (semester_id,),
            )
            return {"message": "Semester deleted successfully"}
        except Exception:
            db.conn.rollback()
            return ({"error": "Semester is still referenced"}, 409)
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
                end as current_status
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
        semester_id = data.get("semester_id")
        period_id = data.get("period_id") or uuid4().hex[:20]
        period_name = data.get("period_name") or "Registration Period"
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not semester_id or not period_id or (not period_name):
            return ({"error": "Missing registration period information"}, 400)
        if not start_date or not end_date:
            return ({"error": "Start date and end date are required"}, 400)
        try:
            start_date = date.fromisoformat(str(start_date)[:10]).isoformat()
            end_date = date.fromisoformat(str(end_date)[:10]).isoformat()
        except ValueError:
            return ({"error": "Start date and end date must be valid dates"}, 400)
        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        db = get_db()
        try:
            semester = db.fetch_one(
                """
            select start_date, end_date
            from semesters
            where semester_id = %s
        """,
                (semester_id,),
            )
            if not semester:
                return ({"error": "Semester not found"}, 404)
            if start_date < str(semester["start_date"])[:10] or end_date > str(semester["end_date"])[:10]:
                return ({"error": "Registration period must fall within the semester"}, 400)
            db.execute_query(
                """
            insert into registration_periods
            (
                period_id,
                semester_id,
                period_name,
                start_date,
                end_date,
                drop_start_date,
                drop_end_date
            )
            values (%s, %s, %s, %s, %s, %s, %s)
        """,
                (period_id, semester_id, period_name, start_date, end_date, start_date, end_date),
            )
            return ({"message": "Registration period created successfully"}, 201)
        except Exception:
            db.conn.rollback()
            return ({"error": "Invalid registration period"}, 409)
        finally:
            db.close()

    def update_period(self, period_id, data):
        """Update a registration period."""
        data = data or {}
        semester_id = data.get("semester_id")
        period_name = data.get("period_name") or "Registration Period"
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not semester_id or not period_name:
            return ({"error": "Missing registration period information"}, 400)
        if not start_date or not end_date:
            return ({"error": "Start date and end date are required"}, 400)
        try:
            start_date = date.fromisoformat(str(start_date)[:10]).isoformat()
            end_date = date.fromisoformat(str(end_date)[:10]).isoformat()
        except ValueError:
            return ({"error": "Start date and end date must be valid dates"}, 400)
        if start_date >= end_date:
            return ({"error": "Start date must be earlier than end date"}, 400)
        db = get_db()
        try:
            semester = db.fetch_one(
                """
            select start_date, end_date
            from semesters
            where semester_id = %s
        """,
                (semester_id,),
            )
            if not semester:
                return ({"error": "Semester not found"}, 404)
            if start_date < str(semester["start_date"])[:10] or end_date > str(semester["end_date"])[:10]:
                return (
                    {"error": "Registration period must fall within the semester"},
                    400,
                )
            db.execute_query(
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
                (semester_id, period_name, start_date, end_date, start_date, end_date, period_id),
            )
            return {"message": "Registration period updated successfully"}
        finally:
            db.close()

    def delete_period(self, period_id):
        """Delete a registration period."""
        db = get_db()
        try:
            db.execute_query(
                """
            delete from registration_periods
            where period_id = %s
        """,
                (period_id,),
            )
            return {"message": "Registration period deleted successfully"}
        except Exception:
            db.conn.rollback()
            return ({"error": "Registration period is still referenced"}, 409)
        finally:
            db.close()

    def generateRegistrationDemandReport(self, query):
        """Get registration demand for courses."""
        period_id = query.get("period_id")
        major_code = query.get("major_code")
        if not period_id:
            return ({"error": "period_id is required"}, 400)
        db = get_db()
        try:
            demand = db.fetch_all(
                """
            select
                c.course_code,
                c.course_name,
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
            left join students s on s.student_id = r.student_id
            where (%s is null or cu.major_code = %s)
            group by c.course_code, c.course_name
            order by c.course_code
        """,
                (major_code, major_code, period_id, major_code, major_code),
            )
            return demand
        finally:
            db.close()

    def demand_students(self, course_code, query):
        """Get students registered for a course in a period."""
        period_id = query.get("period_id")
        major_code = query.get("major_code")
        if not period_id:
            return ({"error": "period_id is required"}, 400)
        db = get_db()
        try:
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
            db.execute_query(
                """
            delete from teaching_assignments
            where assignment_id = %s
        """,
                (assignment_id,),
            )
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
        qualification_id = data.get("qualification_id") or uuid4().hex[:20]
        lecturer_id = data.get("lecturer_id")
        course_code = data.get("course_code")
        if not qualification_id or not lecturer_id or (not course_code):
            return ({"error": "Missing qualification information"}, 400)
        db = get_db()
        try:
            db.execute_query(
                """
            insert into lecturer_qualifications
            (
                qualification_id,
                lecturer_id,
                course_id,
                course_code
            )
            values (%s, %s, (select course_id from courses where course_code=%s), %s)
        """,
                (qualification_id, lecturer_id, course_code, course_code),
            )
            return ({"message": "Qualification added successfully"}, 201)
        except Exception:
            db.conn.rollback()
            return ({"error": "Invalid or duplicate qualification"}, 409)
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
        assignment_id = data.get("assignment_id") or uuid4().hex[:20]
        semester_id = data.get("semester_id")
        lecturer_id = data.get("lecturer_id")
        course_code = data.get("course_code")
        if (
            not assignment_id
            or not semester_id
            or (not lecturer_id)
            or (not course_code)
        ):
            return ({"error": "Missing assignment information"}, 400)
        db = get_db()
        try:
            assignment = TeachingAssignment(
                assignment_id, lecturer_id, course_code, semester_id
            )
            qualified = assignment.isQualified(db)
            if not qualified:
                return ({"error": "Lecturer is not qualified for this course"}, 400)
            assignment.save(db)
            return ({"message": "Lecturer assigned successfully"}, 201)
        except Exception:
            db.conn.rollback()
            return ({"error": "Invalid assignment or duplicate assignment"}, 409)
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
