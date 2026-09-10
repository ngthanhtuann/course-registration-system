"""An assignment links a lecturer, course, and semester."""


class TeachingAssignment:
    """An existing assignment is active; the current API deletes the row when removing an assignment."""

    def __init__(
        self, assignmentID, lecturerId, courseCode, semesterId, status="active"
    ):
        """Create an assignment to record which course a lecturer teaches in which semester."""
        self.assignmentID = assignmentID
        self.lecturerId = lecturerId
        self.courseCode = courseCode
        self.semesterId = semesterId
        self.status = status

    def isQualified(self, db):
        """Only lecturers with configured qualifications may be assigned to a course."""
        qualification = db.fetch_one(
            'select 1 from lecturer_qualifications where lecturer_id=%s and course_id=(select course_id from courses where course_code=%s)',
            (self.lecturerId, self.courseCode),
        )
        if qualification:
            return True
        return False

    def save(self, db):
        """Store the assignment; foreign keys and unique constraints protect data relationships."""
        db.execute_query(
            "insert into teaching_assignments "
            "(assignment_id, semester_id, lecturer_id, course_id) "
            "values (%s,%s,%s,(select course_id from courses where course_code=%s))",
            (
                self.assignmentID,
                self.semesterId,
                self.lecturerId,
                self.courseCode,
            ),
        )
