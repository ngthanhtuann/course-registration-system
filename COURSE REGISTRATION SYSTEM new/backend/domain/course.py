"""Biểu diễn học phần và các điều kiện cho phép đăng ký."""


class Course:
    """Lưu thông tin học phần; kiểm tra môn tiên quyết và sức chứa trong giao dịch."""

    def __init__(
        self,
        courseCode,
        courseName="",
        credit=0,
        maxCapacity=0,
        prerequisiteCourseCode=None,
        recommendedSemester=None,
        semester=None,
    ):
        """Tạo học phần và lưu mã, tên, tín chỉ, sĩ số cùng môn tiên quyết."""
        self.courseCode = courseCode
        self.courseName = courseName
        self.credit = credit
        self.maxCapacity = maxCapacity
        self.prerequisiteCourseCode = prerequisiteCourseCode
        self.recommendedSemester = recommendedSemester
        self.semester = semester

    @staticmethod
    def positiveInteger(value):
        """Kiểm tra số nguyên dương; gọi bằng Course.positiveInteger vì không cần đối tượng."""
        # Python xem True/False là số nguyên 1/0, nhưng chúng không phải tín chỉ hay sĩ số.
        if isinstance(value, bool) or not isinstance(value, (int, str)):
            raise ValueError("Credit and capacity must be positive integers")
        try:
            number = int(value)
        except ValueError as exc:
            raise ValueError("Credit and capacity must be positive integers") from exc
        if number <= 0:
            raise ValueError("Credit and capacity must be positive integers")
        return number

    @classmethod
    def from_row(cls, row):
        """Tạo đối tượng từ bản ghi database; cls là lớp Course đang gọi phương thức."""
        return cls(
            courseCode=row["course_code"],
            courseName=row.get("course_name", ""),
            credit=row.get("credit", 0),
            maxCapacity=row["max_capacity"],
            prerequisiteCourseCode=row.get("prerequisite_course_code"),
            recommendedSemester=row.get("recommended_semester"),
            semester=row.get("semester_id"),
        )

    def checkPrerequisite(self, db, student_id):
        """Cho phép đăng ký khi không có môn tiên quyết hoặc sinh viên đã đạt môn đó."""
        if self.prerequisiteCourseCode is None:
            return True
        passed_registration = db.fetch_one(
            "select 1 from registrations where student_id=%s and course_code=%s and result_status='passed'",
            (student_id, self.prerequisiteCourseCode),
        )
        if passed_registration:
            return True
        return False

    def checkCapacity(self, db, period_id):
        """Kiểm tra chỗ trống; bên gọi phải giữ khóa học phần đến khi commit/rollback."""
        registration_count = db.fetch_one(
            "select count(*) as registered_count from registrations "
            "where course_code=%s and period_id=%s and registration_status='registered'",
            (self.courseCode, period_id),
        )
        return registration_count["registered_count"] < self.maxCapacity
