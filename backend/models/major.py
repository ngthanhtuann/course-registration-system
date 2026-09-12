"""Major model."""


class Major:
    """Store major information and check its courses."""

    def __init__(self, majorCode, majorName=""):
        """Create a Major object."""
        self.majorCode = majorCode
        self.majorName = majorName

    def includesCourse(self, db, course_code):
        """Check whether a course belongs to this major."""
        curriculum_entry = db.fetch_one(
            "select 1 from curriculum where major_code=%s and course_code=%s",
            (self.majorCode, course_code),
        )
        if curriculum_entry:
            return True
        return False
