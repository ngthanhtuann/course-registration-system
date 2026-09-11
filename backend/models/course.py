"""Course model."""


class Course:
    """Store course information and check registration conditions."""

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
        """Create a Course object."""
        self.courseCode = courseCode
        self.courseName = courseName
        self.credit = credit
        self.maxCapacity = maxCapacity
        self.prerequisiteCourseCode = prerequisiteCourseCode
        self.recommendedSemester = recommendedSemester
        self.semester = semester

    @staticmethod
    def positiveInteger(value):
        """Check that a value is a positive integer."""
        # True and False are not valid values here.
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
        """Create a Course object from a database row."""
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
        """Check whether the student passed the prerequisite course."""
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
        """Check whether the course still has available seats."""
        registration_count = db.fetch_one(
            "select count(*) as registered_count from registrations "
            "where course_code=%s and semester_id=(select semester_id from registration_periods where period_id=%s) and registration_status='registered'",
            (self.courseCode, period_id),
        )
        return registration_count["registered_count"] < self.maxCapacity
