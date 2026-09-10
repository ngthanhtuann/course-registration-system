"""Object-oriented business logic for the Lecturer role."""

from database import get_db
from .user import User
from math import isfinite
from .grade import GradeRecord


class Lecturer(User):
    """Lecturer: encapsulates business logic according to the Class Diagram; independent of Flask."""

    def __init__(self, identity=None):
        """Initialize the role from the authenticated identity and inherit User account behavior."""
        super().__init__(identity)
        self.lecturerID = self.identity.get("lecturer_id")

    def viewProfile(self):
        """Read the profile for the current account without allowing access to another user’s profile."""
        user = self.identity
        db = get_db()
        try:
            row = db.fetch_one(
                """select l.lecturer_id, u.user_id, u.username, u.full_name as fullname, u.email, u.role,
            coalesce(array_agg(qc.course_code) filter (where qc.course_code is not null), '{}') as qualifications
            from lecturers l join users u on u.user_id=l.user_id
            left join lecturer_qualifications q on q.lecturer_id=l.lecturer_id
            left join courses qc on qc.course_id=q.course_id
            where l.user_id=%s group by l.lecturer_id,u.user_id,u.username,u.full_name,u.email,u.role""",
                (user["user_id"],),
            )
            if row:
                self._loadAccount(row)
                self.lecturerID = row["lecturer_id"]
                return row, 200
            return {"error": "lecturer profile not found"}, 404
        finally:
            db.close()

    def viewSemesters(self):
        """Get the semester list so the user can select the data scope."""
        db = get_db()
        try:
            return db.fetch_all(
                "select semester_id, semester_name, start_date, end_date, status from semesters order by start_date desc"
            )
        finally:
            db.close()

    def viewTeachingCourse(self, query):
        """Get courses assigned to the lecturer for the semester."""
        lecturer = self.identity
        semester_id = query.get("semester_id")
        if not semester_id:
            return ({"error": "semester_id is required"}, 400)
        db = get_db()
        try:
            return db.fetch_all(
                """
            select ta.assignment_id, c.course_code, c.course_name, c.credit,
                   (select ref.course_code from courses ref where ref.course_id=c.prerequisite_course_id) as prerequisite_course_code,
                   (select count(*) from registrations r join registration_periods rp on rp.period_id=r.period_id
                    where r.course_id=c.course_id and rp.semester_id=ta.semester_id and lower(r.status::text)='registered') as student_count
            from teaching_assignments ta
            join lecturers l on l.lecturer_id=ta.lecturer_id
            join courses c on c.course_id=ta.course_id
            where l.user_id=%s and ta.semester_id=%s
            order by c.course_code
        """,
                (lecturer["user_id"], semester_id),
            )
        finally:
            db.close()

    def viewRegisteredStudents(self, course_code, query):
        """Verify the assignment before retrieving the list of registered students."""
        lecturer = self.identity
        semester_id = query.get("semester_id")
        db = get_db()
        try:
            allowed = db.fetch_one(
                """
            select 1 from teaching_assignments ta
            join lecturers l on l.lecturer_id=ta.lecturer_id
            where l.user_id=%s and ta.semester_id=%s and (select ref.course_code from courses ref where ref.course_id=ta.course_id)=%s
        """,
                (lecturer["user_id"], semester_id, course_code),
            )
            if not allowed:
                return ({"error": "course is not assigned to this lecturer"}, 403)
            return db.fetch_all(
                """
            select st.student_id, u.full_name as fullname, u.email,
                   r.registration_id, r.grade, r.result_status,
                   case when c.prerequisite_course_id is null then 'Satisfied'
                        when exists (select 1 from registrations pr where pr.student_id=st.student_id and pr.course_id=c.prerequisite_course_id and pr.result_status='passed') then 'Satisfied'
                        else 'Not Satisfied' end as prerequisite_status
            from registrations r
            join students st on st.student_id=r.student_id
            join users u on u.user_id=st.user_id
            join courses c on c.course_id=r.course_id
            join registration_periods rp on rp.period_id=r.period_id
            where c.course_code=%s and rp.semester_id=%s and lower(r.status::text)='registered'
            order by st.student_id
        """,
                (course_code, semester_id),
            )
        finally:
            db.close()

    def manageStudentGrade(self, registration_id, data):
        """Verify the assignment, deadline, and grade before updating the result."""
        lecturer = self.identity
        data = data or {}
        grade = data.get("grade")
        if grade is None:
            return ({"error": "grade is required"}, 400)
        try:
            grade = float(grade)
        except (TypeError, ValueError):
            return ({"error": "grade must be a number"}, 400)
        if not isfinite(grade) or grade < 0 or grade > 10:
            return ({"error": "grade must be between 0 and 10"}, 400)
        db = get_db()
        try:
            row = db.fetch_one(
                """
            select r.registration_id, rp.semester_id
            from registrations r
            join registration_periods rp on rp.period_id=r.period_id
            join teaching_assignments ta on ta.course_id=r.course_id and ta.semester_id=rp.semester_id
            join lecturers l on l.lecturer_id=ta.lecturer_id
            where r.registration_id=%s and l.user_id=%s and lower(r.status::text)='registered' for update of r, ta
        """,
                (registration_id, lecturer["user_id"]),
            )
            if not row:
                return (
                    {
                        "error": "student is not registered in a course assigned to this lecturer"
                    },
                    403,
                )
            periods = db.fetch_all(
                "select end_date < current_date as ended from registration_periods where semester_id=%s for update",
                (row["semester_id"],),
            )
            # Only enter grades after all registration periods for the semester have ended.
            if not periods:
                return ({"error": "registration period has not ended"}, 400)
            for period in periods:
                if not period["ended"]:
                    return ({"error": "registration period has not ended"}, 400)
            grade_record = GradeRecord(grade)
            result_status = grade_record.calculateResultStatus()
            db.execute_query(
                "update registrations set grade=%s, result_status=%s where registration_id=%s",
                (grade, result_status, registration_id),
            )
            return {
                "message": "grade saved successfully",
                "result_status": result_status,
            }
        finally:
            db.close()
