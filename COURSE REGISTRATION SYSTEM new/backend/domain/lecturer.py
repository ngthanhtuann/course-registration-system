"""Nghiệp vụ hướng đối tượng cho vai trò Lecturer."""

from database import get_db
from .user import User
from math import isfinite
from .grade_record import GradeRecord


class Lecturer(User):
    """Lecturer: đóng gói nghiệp vụ theo Class Diagram; không phụ thuộc Flask."""

    def __init__(self, identity=None):
        """Khởi tạo vai trò từ danh tính đã xác thực và kế thừa hành vi tài khoản của User."""
        super().__init__(identity)
        self.lecturerID = self.identity.get("lecturer_id")

    def viewProfile(self):
        """Đọc hồ sơ theo tài khoản hiện tại, không cho truy cập hồ sơ người khác."""
        user = self.identity
        db = get_db()
        try:
            row = db.fetch_one(
                """select l.lecturer_id, u.user_id, u.username, u.fullname, u.email, u.role,
            coalesce(array_agg(q.course_code) filter (where q.course_code is not null), '{}') as qualifications
            from lecturers l join users u on u.user_id=l.user_id
            left join lecturer_qualifications q on q.lecturer_id=l.lecturer_id
            where l.user_id=%s group by l.lecturer_id,u.user_id,u.username,u.fullname,u.email,u.role""",
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
        """Lấy danh sách học kỳ để người dùng chọn phạm vi dữ liệu."""
        db = get_db()
        try:
            return db.fetch_all(
                "select semester_id, semester_name, start_date, end_date, status from semesters order by start_date desc"
            )
        finally:
            db.close()

    def viewTeachingCourse(self, query):
        """Lấy các học phần được phân công cho giảng viên trong học kỳ."""
        lecturer = self.identity
        semester_id = query.get("semester_id")
        if not semester_id:
            return ({"error": "semester_id is required"}, 400)
        db = get_db()
        try:
            return db.fetch_all(
                """
            select ta.assignment_id, c.course_code, c.course_name, c.credit,
                   c.prerequisite_course_code,
                   (select count(*) from registrations r join registration_periods rp on rp.period_id=r.period_id
                    where r.course_code=c.course_code and rp.semester_id=ta.semester_id and r.registration_status='registered') as student_count
            from teaching_assignments ta
            join lecturers l on l.lecturer_id=ta.lecturer_id
            join courses c on c.course_code=ta.course_code
            where l.user_id=%s and ta.semester_id=%s
            order by c.course_code
        """,
                (lecturer["user_id"], semester_id),
            )
        finally:
            db.close()

    def viewRegisteredStudents(self, course_code, query):
        """Kiểm tra phân công trước khi lấy danh sách sinh viên đăng ký."""
        lecturer = self.identity
        semester_id = query.get("semester_id")
        db = get_db()
        try:
            allowed = db.fetch_one(
                """
            select 1 from teaching_assignments ta
            join lecturers l on l.lecturer_id=ta.lecturer_id
            where l.user_id=%s and ta.semester_id=%s and ta.course_code=%s
        """,
                (lecturer["user_id"], semester_id, course_code),
            )
            if not allowed:
                return ({"error": "course is not assigned to this lecturer"}, 403)
            return db.fetch_all(
                """
            select st.student_id, u.fullname, u.email,
                   r.registration_id, r.grade, r.result_status,
                   case when c.prerequisite_course_code is null then 'Satisfied'
                        when exists (select 1 from registrations pr where pr.student_id=st.student_id and pr.course_code=c.prerequisite_course_code and pr.result_status='passed') then 'Satisfied'
                        else 'Not Satisfied' end as prerequisite_status
            from registrations r
            join students st on st.student_id=r.student_id
            join users u on u.user_id=st.user_id
            join courses c on c.course_code=r.course_code
            join registration_periods rp on rp.period_id=r.period_id
            where r.course_code=%s and rp.semester_id=%s and r.registration_status='registered'
            order by st.student_id
        """,
                (course_code, semester_id),
            )
        finally:
            db.close()

    def manageStudentGrade(self, registration_id, data):
        """Kiểm tra phân công, thời hạn và điểm trước khi cập nhật kết quả."""
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
            join teaching_assignments ta on ta.course_code=r.course_code and ta.semester_id=rp.semester_id
            join lecturers l on l.lecturer_id=ta.lecturer_id
            where r.registration_id=%s and l.user_id=%s and r.registration_status='registered' for update of r, ta
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
            # Chỉ nhập điểm khi tất cả đợt đăng ký của học kỳ đã kết thúc.
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
