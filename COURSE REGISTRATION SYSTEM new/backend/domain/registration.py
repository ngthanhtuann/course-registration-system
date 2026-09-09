"""Đối tượng đăng ký liên kết sinh viên, học phần, đợt đăng ký và điểm."""

from uuid import uuid4


class Registration:
    """Lưu thông tin đăng ký học phần và điểm của một sinh viên."""

    def __init__(
        self,
        studentId,
        courseCode,
        periodId,
        registrationId=None,
        registrationStatus="registered",
        gradeRecord=None,
    ):
        """Tạo đăng ký liên kết sinh viên, học phần, đợt đăng ký và điểm nếu đã có."""
        self.studentId = studentId
        self.courseCode = courseCode
        self.periodId = periodId
        self.registrationId = registrationId
        self.registrationStatus = registrationStatus
        self.gradeRecord = gradeRecord

    def saveRegistration(self, db):
        """Tạo hoặc kích hoạt lại đăng ký đã hủy trong giao dịch do bên gọi quản lý."""
        existing = db.fetch_one(
            "select registration_id from registrations where student_id=%s and period_id=%s and course_code=%s",
            (self.studentId, self.periodId, self.courseCode),
        )
        if existing:
            self.registrationId = existing["registration_id"]
            db.execute(
                "update registrations set registration_status='registered', status='REGISTERED'::registration_status, "
                "grade=null, result_status=null where registration_id=%s",
                (self.registrationId,),
            )
        else:
            if not self.registrationId:
                self.registrationId = uuid4().hex
            # Cột registration_id trong database cho phép tối đa 20 ký tự.
            self.registrationId = self.registrationId[:20]
            db.execute(
                "insert into registrations "
                "(registration_id, student_id, course_id, semester_id, status, period_id, course_code, registration_status) "
                "values (%s, %s, (select course_id from courses where course_code=%s), "
                "(select semester_id from registration_periods where period_id=%s), "
                "'REGISTERED'::registration_status, %s, %s, 'registered')",
                (
                    self.registrationId,
                    self.studentId,
                    self.courseCode,
                    self.periodId,
                    self.periodId,
                    self.courseCode,
                ),
            )
        self.registrationStatus = "registered"
        self.gradeRecord = None
        return self.registrationId

    def updateRegistrationStatus(self, db, status):
        """Cập nhật trạng thái hợp lệ; bên gọi kiểm tra chủ sở hữu và thời hạn trước."""
        if status not in ("registered", "dropped"):
            raise ValueError("invalid registration status")
        db.execute(
            "update registrations set registration_status=%s, status=%s::registration_status where registration_id=%s",
            (status, status.upper(), self.registrationId),
        )
        self.registrationStatus = status
