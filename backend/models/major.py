"""Represent a major and the major–course relationship through the curriculum."""


class Major:
    """A major has many courses; a course may belong to multiple majors."""

    def __init__(self, majorCode, majorName=""):
        """Create a major with a major code and name."""
        self.majorCode = majorCode
        self.majorName = majorName

    def includesCourse(self, db, course_code):
        """Determine whether a course belongs to the major’s curriculum."""
        curriculum_entry = db.fetch_one(
            'select 1 from curriculum where major_id=(select major_id from majors where major_code=%s) and course_id=(select course_id from courses where course_code=%s)',
            (self.majorCode, course_code),
        )
        if curriculum_entry:
            return True
        return False
