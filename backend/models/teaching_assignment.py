"""Teaching assignment model."""


class TeachingAssignment:
    """Store a lecturer assignment for a course and semester."""

    def __init__(
        self, assignmentID, lecturerId, courseCode, semesterId, status="active"
    ):
        """Create a TeachingAssignment object."""
        self.assignmentID = assignmentID
        self.lecturerId = lecturerId
        self.courseCode = courseCode
        self.semesterId = semesterId
        self.status = status

    def isQualified(self, db):
        """Check whether the lecturer can teach the course."""
        qualification = db.fetch_one(
            "select 1 from lecturer_qualifications q "
            "join lecturers l on l.lecturer_id=q.lecturer_id "
            "join users u on u.user_id=l.user_id "
            "where q.lecturer_id=%s and q.course_code=%s and u.active_status=true "
            "for share of q, u",
            (self.lecturerId, self.courseCode),
        )
        if qualification:
            return True
        return False

    def save(self, db):
        """Save the teaching assignment to the database."""
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
