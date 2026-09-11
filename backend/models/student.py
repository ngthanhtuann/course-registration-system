"""Functions for the Student role."""

from database import get_db
from .user import User
from .course import Course
from .major import Major
from .registration import Registration
from .registration_period import RegistrationPeriod


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
                "select rp.*, case when current_date < rp.start_date then 'upcoming' when current_date <= rp.end_date then 'open' else 'closed' end as current_status from registration_periods rp order by rp.start_date desc"
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
        period_id = query.get("period_id")
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
            select c.course_code, c.course_name, c.credit,
                   c.prerequisite_course_code, pc.course_name as prerequisite_name,
                   cu.recommended_semester, c.max_capacity,
                   c.max_capacity - count(r.registration_id) filter (where r.registration_status='registered') as available_seats,
                   case when c.prerequisite_course_code is null then 'N/A'
                        when exists (select 1 from registrations pr where pr.student_id=s.student_id and pr.course_code=c.prerequisite_course_code and pr.result_status='passed') then 'Satisfied'
                        else 'Not Satisfied' end as prerequisite_status,
                   case when exists (select 1 from registrations sr where sr.student_id=s.student_id and sr.course_code=c.course_code and sr.semester_id=(select semester_id from registration_periods where period_id=%s) and sr.registration_status='registered') then 'Registered' else 'Available' end as reg_status
            from students s
            join curriculum cu on cu.major_code=s.major_code
            join courses c on c.course_code=cu.course_code
            left join courses pc on pc.course_code=c.prerequisite_course_code
            left join registrations r on r.course_code=c.course_code and r.semester_id=(select semester_id from registration_periods where period_id=%s)
            where s.student_id=%s
              and (c.course_code ilike %s or c.course_name ilike %s)
              and not exists (
                  select 1 from registrations r2
                  where r2.student_id=s.student_id and r2.course_code=c.course_code and r2.semester_id=(select semester_id from registration_periods where period_id=%s)
                    and r2.registration_status='registered'
              )
              and not exists (
                  select 1 from registrations r3
                  where r3.student_id=s.student_id and r3.course_code=c.course_code
                    and r3.result_status='passed'
              )
            group by c.course_code, c.course_name, c.credit, c.prerequisite_course_code,
                     pc.course_name, cu.recommended_semester, c.max_capacity, s.student_id
            order by c.course_code
        """,
                (
                    period_id,
                    period_id,
                    student_record["student_id"],
                    f"%{search}%",
                    f"%{search}%",
                    period_id,
                ),
            )
        finally:
            db.close()

    def registerCourse(self, data):
        """Check registration conditions and register the student for a course."""
        # 1. Get the selected course and registration period.
        student = self.identity
        data = data or {}
        course_code = data.get("course_code")
        period_id = data.get("period_id")
        if not course_code or not period_id:
            return ({"error": "course_code and period_id are required"}, 400)
        db = get_db()
        try:
            # 2. Lock the course row before checking available seats.
            course = db.fetch_one(
                "select * from courses where course_code=%s for update", (course_code,)
            )
            if not course:
                db.conn.rollback()
                return ({"error": "course not found"}, 404)
            # 3. Check that registration is open.
            period = db.fetch_one(
                """select * from registration_periods
            where period_id=%s and current_date between start_date and end_date for update""",
                (period_id,),
            )
            if not period:
                db.conn.rollback()
                return ({"error": "registration period is not open"}, 400)
            student_record = db.fetch_one(
                "select student_id, major_code from students where user_id=%s",
                (student["user_id"],),
            )
            if not student_record:
                db.conn.rollback()
                return ({"error": "student profile not found"}, 404)
            # 4. Check that the course belongs to the student curriculum.
            self.studentID = student_record["student_id"]
            self.major = Major(student_record["major_code"])
            eligible = self.major.includesCourse(db, course_code)
            if not eligible:
                db.conn.rollback()
                return (
                    {"error": "course does not belong to student's curriculum"},
                    400,
                )
            # 5. Check duplicate registration and completed courses.
            duplicate = db.fetch_one(
                """select 1 from registrations
            where student_id=%s and course_code=%s and semester_id=(select semester_id from registration_periods where period_id=%s) and registration_status='registered'""",
                (student_record["student_id"], course_code, period_id),
            )
            if duplicate:
                db.conn.rollback()
                return ({"error": "student is already registered for this course"}, 409)
            passed = db.fetch_one(
                """select 1 from registrations
            where student_id=%s and course_code=%s and result_status='passed'""",
                (student_record["student_id"], course_code),
            )
            if passed:
                db.conn.rollback()
                return ({"error": "student has already completed this course"}, 400)
            # 6. Check prerequisite and course capacity.
            course_object = Course.from_row(course)
            if not course_object.checkPrerequisite(db, self.studentID):
                db.conn.rollback()
                return ({"error": "prerequisite is not satisfied"}, 400)
            if not course_object.checkCapacity(db, period_id):
                db.conn.rollback()
                return ({"error": "course capacity has been reached"}, 409)
            # 7. Save the registration.
            registration = Registration(
                self.studentID, course_code, period_id, data.get("registration_id")
            )
            registration_id = registration.saveRegistration(db)
            db.conn.commit()
            return (
                {
                    "message": "course registered successfully",
                    "registration_id": registration_id,
                },
                201,
            )
        except Exception as exc:
            # Undo database changes if registration fails.
            db.conn.rollback()
            return ({"error": "registration failed: duplicate registration or invalid data"}, 409)
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
                   (c.max_capacity - (select count(*) from registrations rr where rr.course_code=r.course_code and rr.semester_id=r.semester_id and rr.registration_status='registered')) as available_seats,
                   rp.start_date as registration_start_date,
                   rp.end_date as registration_end_date,
                   case when current_date < rp.start_date then 'upcoming'
                        when current_date <= rp.end_date then 'open'
                        else 'closed' end as current_registration_status
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
        """Drop a course while the registration period is open."""
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
                   rp.drop_start_date as start_date, rp.drop_end_date as end_date
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
            period = RegistrationPeriod("", row["start_date"], row["end_date"])
            period_status = period.updateRegistrationStatus()
            if period_status != "open":
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
            where st.user_id=%s and (%s is null or s.semester_id=%s)
            order by s.start_date desc, c.course_code
        """,
                (student["user_id"], semester_id, semester_id),
            )
        finally:
            db.close()
