"""Phân công liên kết giảng viên, học phần và học kỳ."""


class TeachingAssignment:
    """Phân công tồn tại là active; API hiện tại xóa hàng khi gỡ phân công."""

    def __init__(
        self, assignmentID, lecturerId, courseCode, semesterId, status="active"
    ):
        """Tạo phân công để ghi nhận giảng viên dạy học phần nào trong học kỳ nào."""
        self.assignmentID = assignmentID
        self.lecturerId = lecturerId
        self.courseCode = courseCode
        self.semesterId = semesterId
        self.status = status

    def isQualified(self, db):
        """Chỉ giảng viên có chuyên môn đã cấu hình mới được phân công học phần."""
        qualification = db.fetch_one(
            "select 1 from lecturer_qualifications "
            "where lecturer_id=%s and course_code=%s",
            (self.lecturerId, self.courseCode),
        )
        if qualification:
            return True
        return False

    def save(self, db):
        """Lưu phân công; khóa ngoại và ràng buộc unique bảo vệ liên kết dữ liệu."""
        db.execute_query(
            "insert into teaching_assignments "
            "(assignment_id, semester_id, lecturer_id, course_id, course_code) "
            "values (%s,%s,%s,(select course_id from courses where course_code=%s),%s)",
            (
                self.assignmentID,
                self.semesterId,
                self.lecturerId,
                self.courseCode,
                self.courseCode,
            ),
        )
