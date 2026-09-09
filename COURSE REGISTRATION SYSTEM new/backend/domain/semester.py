"""Biểu diễn học kỳ và kiểm tra thời gian chồng lấn."""


class Semester:
    """Lưu thông tin học kỳ và kiểm tra trùng thời gian với học kỳ khác."""

    def __init__(
        self,
        semesterName,
        startDate,
        endDate,
        semesterStatus="upcoming",
        semesterId=None,
    ):
        """Lưu học kỳ; startDate và endDate là các đối tượng ngày của Python."""
        self.semesterName = semesterName
        self.startDate = startDate
        self.endDate = endDate
        self.semesterStatus = semesterStatus
        self.semesterId = semesterId

    def checkOverlap(self, otherSemester):
        """Hai học kỳ chồng lấn khi khoảng thời gian giao nhau; cho phép chạm biên."""
        return (
            self.startDate < otherSemester.endDate
            and self.endDate > otherSemester.startDate
        )

    def overlapsExisting(self, db):
        """Đọc các học kỳ khác và áp dụng cùng quy tắc checkOverlap khi tạo/cập nhật."""
        semester_records = db.fetch_all(
            "select semester_name, start_date, end_date from semesters "
            "where (%s is null or semester_id <> %s)",
            (self.semesterId, self.semesterId),
        )
        for semester_record in semester_records:
            other_semester = Semester(
                semester_record["semester_name"],
                semester_record["start_date"],
                semester_record["end_date"],
            )
            if self.checkOverlap(other_semester):
                return True
        return False
