"""Represent a semester and check for overlapping dates."""


class Semester:
    """Store semester information and check for date overlap with other semesters."""

    def __init__(
        self,
        semesterName,
        startDate,
        endDate,
        semesterStatus="upcoming",
        semesterId=None,
    ):
        """Store the semester; startDate and endDate are Python date objects."""
        self.semesterName = semesterName
        self.startDate = startDate
        self.endDate = endDate
        self.semesterStatus = semesterStatus
        self.semesterId = semesterId

    def checkOverlap(self, otherSemester):
        """Two semesters overlap when their date ranges intersect; touching boundaries are allowed."""
        return (
            self.startDate < otherSemester.endDate
            and self.endDate > otherSemester.startDate
        )

    def overlapsExisting(self, db):
        """Read other semesters and apply the same checkOverlap rule when creating/updating."""
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
