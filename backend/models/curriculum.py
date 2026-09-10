"""Represent a course in a major’s curriculum."""


class Curriculum:
    """Store the major, course, and suggested-semester relationship; persistence is managed by the service."""

    def __init__(self, major_code, course_code, recommended_semester=None, curriculum_id=None):
        """Initialize a curriculum entry independently of the HTTP layer."""
        self.major_code = major_code
        self.course_code = course_code
        self.recommended_semester = recommended_semester
        self.curriculum_id = curriculum_id
