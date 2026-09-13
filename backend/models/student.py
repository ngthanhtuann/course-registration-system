"""Functions for the Student role."""

import psycopg2

from database import get_db
from uuid import uuid4
from .user import User
from .course import Course
from .major import Major
from .registration import Registration


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


class Student(User):
    """Student functions for the course registration system."""

    def __init__(self, identity=None):
        """Create a Student object from user information."""
        super().__init__(identity)
        self.studentID = self.identity.get("student_id")
        self.dateOfBirth = self.identity.get("dob")
        self.major = None
        major_code = self.identity.get("major_code")
        if major_code:
            self.major = Major(major_code)

    def viewProfile(self):
        """Get the student profile."""
        user = self.identity
        db = get_db()
        try:
            row = db.fetch_one(
                """select s.student_id, s.date_of_birth as dob, s.major_code, u.user_id, u.username, u.full_name as fullname, u.email, u.role
            from students s join users u on u.user_id=s.user_id where s.user_id=%s""",
                (user["user_id"],),
            )
            if row:
                self._loadAccount(row)
                self.studentID = row["student_id"]
                self.dateOfBirth = row["dob"]
                self.major = Major(row["major_code"])
                return row, 200
            return {"error": "student profile not found"}, 404
        finally:
            db.close()

    def viewSemesters(self):
        """Get all semesters."""
        db = get_db()
        try:
            return db.fetch_all(
                "select semester_id, semester_name, start_date, end_date, status from semesters order by start_date desc"
            )
        finally:
            db.close()

    def viewRegistrationPeriods(self):
        """Get registration periods and their current status."""
        db = get_db()
        try:
            return db.fetch_all(
                "select rp.*, case when current_date < rp.start_date then 'upcoming' when current_date <= rp.end_date then 'open' else 'closed' end as current_status, "
                "case when current_date < rp.drop_start_date then 'upcoming' when current_date <= rp.drop_end_date then 'open' else 'closed' end as current_drop_status "
                "from registration_periods rp order by rp.start_date desc, rp.period_id"
            )
        finally:
            db.close()

    def viewCurriculum(self):
        """Get the curriculum for the student major."""
        user = self.identity
        db = get_db()
        try:
            return db.fetch_all(
                """select cu.curriculum_id, cu.major_code, cu.course_code, c.course_name, c.credit,
            c.prerequisite_course_code, cu.recommended_semester from students s
            join curriculum cu on cu.major_code=s.major_code join courses c on c.course_code=cu.course_code
            where s.user_id=%s order by cu.recommended_semester, cu.course_code""",
                (user["user_id"],),
            )
        finally:
            db.close()

    def viewCourses(self, query):
        """Get courses with prerequisite and seat information."""
        student = self.identity
        search = query.get("search", "").strip()
        period_id = query.get("period_id") or None
        db = get_db()
        try:
            if period_id is not None:
                period = db.fetch_one(
                    "select period_id, semester_id from registration_periods where period_id=%s",
                    (period_id,),
                )
                if not period:
                    return ({"error": "registration period not found"}, 404)
                semester_id = period["semester_id"]
            else:
                # View Courses has no period selector. Use one academic semester
                # for both registration visibility and capacity calculations.
                semester = db.fetch_one(
                    "select semester_id from semesters order by "
                    "case when current_date between start_date and end_date then 0 "
                    "when start_date > current_date then 1 else 2 end, "
                    "case when start_date > current_date then start_date end asc, "
                    "start_date desc, semester_id limit 1"
                )
                semester_id = semester["semester_id"] if semester else None
            student_record = db.fetch_one(
                "select student_id from students where user_id=%s",
                (student["user_id"],),
            )
            if not student_record:
                return ({"error": "student profile not found"}, 404)
            return db.fetch_all(
                """
            select c.course_code, c.course_name, c.credit,
                   c.prerequisite_course_code, pc.course_name as prerequisite_name,
                   cu.recommended_semester, c.max_capacity, %s::varchar as semester_id,
                   greatest(0, c.max_capacity - count(r.registration_id) filter (where r.status='REGISTERED')) as available_seats,
                   case when c.prerequisite_course_code is null then 'N/A'
                        when exists (select 1 from registrations pr where pr.student_id=s.student_id and pr.course_code=c.prerequisite_course_code and pr.result_status='passed') then 'Satisfied'
                        else 'Not Satisfied' end as prerequisite_status,
                   'Available' as reg_status
            from students s
            join curriculum cu on cu.major_code=s.major_code
            join courses c on c.course_code=cu.course_code
            left join courses pc on pc.course_code=c.prerequisite_course_code
            left join registrations r on r.course_id=c.course_id and r.semester_id=%s
            where s.student_id=%s
              and (c.course_code ilike %s or c.course_name ilike %s)
              and (not %s or not exists (
                  select 1 from registrations r2
                  where r2.student_id=s.student_id and r2.course_id=c.course_id
                    and (%s is null or r2.semester_id=%s)
                    and r2.status='REGISTERED'
              ))
              and (not %s or not exists (
                  select 1 from registrations r3
                  where r3.student_id=s.student_id and r3.course_code=c.course_code
                    and r3.result_status='passed'
              ))
            group by c.course_id, c.course_code, c.course_name, c.credit, c.prerequisite_course_code,
                     pc.course_name, cu.recommended_semester, c.max_capacity, s.student_id
            order by c.course_code
        """,
                (
                    semester_id,
                    semester_id,
                    student_record["student_id"],
                    f"%{search}%",
                    f"%{search}%",
                    period_id is not None,
                    semester_id,
                    semester_id,
                    period_id is not None,
                ),
            )
        finally:
            db.close()

    def registerCourse(self, data):
        """Validate and register a course with fewer database round-trips."""
        student = self.identity
        data = data or {}

        try:
            course_code = _required_text(data.get("course_code"), "course_code")
            period_id = _required_text(data.get("period_id"), "period_id")
            registration_id = _optional_text(
                data.get("registration_id"),
                "registration_id",
            )
        except ValueError as exc:
            return ({"error": str(exc)}, 400)

        if registration_id is None:
            registration_id = uuid4().hex[:20]
        else:
            registration_id = registration_id[:20]

        db = get_db()
        try:
            context = db.fetch_one(
                """
                select
                    c.course_id,
                    c.course_code,
                    c.max_capacity,
                    c.prerequisite_course_code,
                    rp.period_id,
                    rp.semester_id,
                    s.student_id,
                    s.major_code,
                    case
                        when rp.period_id is null then false
                        else current_date between rp.start_date and rp.end_date
                    end as period_open,
                    exists (
                        select 1
                        from curriculum cu
                        where cu.major_code = s.major_code
                          and cu.course_code = c.course_code
                    ) as eligible,
                    exists (
                        select 1
                        from registrations r
                        where r.student_id = s.student_id
                          and r.course_id = c.course_id
                          and r.semester_id = rp.semester_id
                          and r.status = 'REGISTERED'
                    ) as duplicate_registration,
                    exists (
                        select 1
                        from registrations r
                        where r.student_id = s.student_id
                          and r.course_id = c.course_id
                          and r.result_status = 'passed'
                    ) as already_passed,
                    case
                        when c.prerequisite_course_code is null then true
                        else exists (
                            select 1
                            from registrations pr
                            where pr.student_id = s.student_id
                              and pr.course_code = c.prerequisite_course_code
                              and pr.result_status = 'passed'
                        )
                    end as prerequisite_satisfied,
                    coalesce((
                        select count(*)
                        from registrations cr
                        where cr.course_id = c.course_id
                          and cr.semester_id = rp.semester_id
                          and cr.status = 'REGISTERED'
                    ), 0) as registered_count
                from (select 1) seed
                left join courses c
                    on c.course_code = %s
                left join registration_periods rp
                    on rp.period_id = %s
                left join students s
                    on s.user_id = %s
                """,
                (course_code, period_id, student["user_id"]),
            )

            if not context.get("course_id"):
                return ({"error": "course not found"}, 404)
            if not context.get("period_id"):
                return ({"error": "registration period not found"}, 404)
            if not context.get("student_id"):
                return ({"error": "student profile not found"}, 404)
            if not context.get("period_open"):
                return ({"error": "registration period is not open"}, 400)
            if not context.get("eligible"):
                return ({"error": "course does not belong to student's curriculum"}, 400)
            if context.get("duplicate_registration"):
                return ({"error": "student is already registered for this course"}, 409)
            if context.get("already_passed"):
                return ({"error": "student has already completed this course"}, 400)
            if not context.get("prerequisite_satisfied"):
                return ({"error": "prerequisite is not satisfied"}, 400)
            if int(context.get("registered_count") or 0) >= int(context["max_capacity"]):
                return ({"error": "course capacity has been reached"}, 409)

            saved = db.fetch_one(
                """
                insert into registrations
                    (registration_id, student_id, course_id, semester_id,
                     status, period_id, course_code)
                values
                    (%s, %s, %s, %s,
                     'REGISTERED'::registration_status_type, %s, %s)
                on conflict (student_id, semester_id, course_id)
                do update set
                    status = 'REGISTERED'::registration_status_type,
                    period_id = excluded.period_id,
                    grade = null,
                    result_status = null
                where registrations.status = 'DROPPED'
                returning registration_id
                """,
                (
                    registration_id,
                    context["student_id"],
                    context["course_id"],
                    context["semester_id"],
                    period_id,
                    course_code,
                ),
            )

            if not saved:
                db.conn.rollback()
                return ({"error": "student is already registered for this course"}, 409)
            db.conn.commit()
            return (
                {
                    "message": "course registered successfully",
                    "registration_id": saved["registration_id"],
                },
                201,
            )

        except (psycopg2.IntegrityError, psycopg2.errors.RaiseException):
            db.conn.rollback()
            return (
                {"error": "registration conflicts with existing data or course capacity"},
                409,
            )
        except psycopg2.Error:
            db.conn.rollback()
            raise
        finally:
            db.close()

    def viewRegistrationStatus(self, query):
        """Get the student registration status for a semester."""
        student = self.identity
        semester_id = query.get("semester_id")
        db = get_db()
        try:
            return db.fetch_all(
                """
            select r.registration_id, c.course_code, c.course_name, c.credit,
                   initcap(r.registration_status) as status, c.max_capacity,
                   greatest(0, c.max_capacity - (select count(*) from registrations rr where rr.course_id=r.course_id and rr.semester_id=r.semester_id and rr.status='REGISTERED')) as available_seats,
                   r.period_id, r.semester_id, rp.period_name,
                   rp.start_date as registration_start_date,
                   rp.end_date as registration_end_date,
                   rp.drop_start_date, rp.drop_end_date,
                   case when current_date < rp.start_date then 'upcoming'
                        when current_date <= rp.end_date then 'open'
                        else 'closed' end as current_registration_status,
                   case when current_date < rp.drop_start_date then 'upcoming'
                        when current_date <= rp.drop_end_date then 'open'
                        else 'closed' end as current_drop_status
            from registrations r
            join students s on s.student_id=r.student_id
            join courses c on c.course_code=r.course_code
            join registration_periods rp on rp.period_id=r.period_id
            where s.user_id=%s and (%s is null or rp.semester_id=%s)
            order by rp.start_date desc, c.course_code
        """,
                (student["user_id"], semester_id, semester_id),
            )
        finally:
            db.close()

    def dropCourse(self, registration_id):
        """Drop a course while the drop period is open."""
        student = self.identity
        db = get_db()
        try:
            db.fetch_one(
                "select c.course_id from courses c join registrations r on r.course_id=c.course_id "
                "join students s on s.student_id=r.student_id "
                "where r.registration_id=%s and s.user_id=%s for update of c",
                (registration_id, student["user_id"]),
            )
            row = db.fetch_one(
                """
            select r.registration_id, r.registration_status, s.student_id, r.course_code, r.period_id,
                   current_date between rp.drop_start_date and rp.drop_end_date as can_drop
            from registrations r
            join students s on s.student_id=r.student_id
            join registration_periods rp on rp.period_id=r.period_id
            where r.registration_id=%s and s.user_id=%s for update of r, rp
        """,
                (registration_id, student["user_id"]),
            )
            if not row:
                return ({"error": "registration not found"}, 404)
            if row["registration_status"] != "registered":
                return ({"error": "course is not currently registered"}, 400)
            if not row["can_drop"]:
                return ({"error": "drop period is not open"}, 400)
            registration = Registration(
                row["student_id"], row["course_code"], row["period_id"], registration_id
            )
            registration.updateRegistrationStatus(db, "dropped")
            db.conn.commit()
            return {"message": "course dropped successfully"}
        finally:
            db.close()

    def viewGrades(self, query):
        """Get the student grades for a semester."""
        student = self.identity
        semester_id = query.get("semester_id")
        db = get_db()
        try:
            student_record = db.fetch_one(
                "select student_id from students where user_id=%s",
                (student["user_id"],),
            )
            if not student_record:
                return ({"error": "student profile not found"}, 404)
            return db.fetch_all(
                """
            select c.course_code, c.course_name, c.credit, r.grade,
                   s.semester_name,
                   case when r.grade is null then null
                        when r.grade >= 5 then 'passed'
                        else 'not passed' end as result_status
            from registrations r
            join students st on st.student_id=r.student_id
            join courses c on c.course_code=r.course_code
            join registration_periods rp on rp.period_id=r.period_id
            join semesters s on s.semester_id=rp.semester_id
            where st.user_id=%s
              and r.registration_status='registered'
              and (%s is null or s.semester_id=%s)
            order by s.start_date desc, c.course_code
        """,
                (student["user_id"], semester_id, semester_id),
            )
        finally:
            db.close()
