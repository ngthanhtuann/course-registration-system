"""Represent a course and the conditions that allow registration."""


class Course:
    """Store course information; check prerequisites and capacity within the transaction."""

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
        """Create a course and store its code, name, credits, capacity, and prerequisite."""
        self.courseCode = courseCode
        self.courseName = courseName
        self.credit = credit
        self.maxCapacity = maxCapacity
        self.prerequisiteCourseCode = prerequisiteCourseCode
        self.recommendedSemester = recommendedSemester
        self.semester = semester

    @staticmethod
    def positiveInteger(value):
        """Check for a positive integer; call via Course.positiveInteger because no object instance is needed."""
        # Python treats True/False as integers 1/0, but they are not valid credits or capacity values.
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
        """Create an object from a database record; cls is the Course class invoking the method."""
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
        """Allow registration when there is no prerequisite or the student has passed it."""
        if self.prerequisiteCourseCode is None:
            return True
        passed_registration = db.fetch_one(
            "select 1 from registrations where student_id=%s and course_id=(select course_id from courses where course_code=%s) and result_status='passed'",
            (student_id, self.prerequisiteCourseCode),
        )
        if passed_registration:
            return True
        return False

    def checkCapacity(self, db, period_id):
        """Check available seats; the caller must keep the course lock until commit/rollback."""
        registration_count = db.fetch_one(
            "select count(*) as registered_count from registrations where course_id=(select course_id from courses where course_code=%s) and period_id=%s and status='REGISTERED'",
            (self.courseCode, period_id),
        )
        return registration_count["registered_count"] < self.maxCapacity
