"""Curriculum model."""


class Curriculum:
    """Store one course in a major curriculum."""

    def __init__(self, major_code, course_code, recommended_semester=None, curriculum_id=None):
        """Create a Curriculum object."""
        self.major_code = major_code
        self.course_code = course_code
        self.recommended_semester = recommended_semester
        self.curriculum_id = curriculum_id
