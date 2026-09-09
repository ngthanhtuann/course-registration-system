"""Biểu diễn ngành học và quan hệ ngành–học phần qua chương trình đào tạo."""


class Major:
    """Ngành có nhiều học phần; một học phần có thể thuộc nhiều ngành."""

    def __init__(self, majorCode, majorName=""):
        """Tạo ngành học với mã ngành và tên ngành."""
        self.majorCode = majorCode
        self.majorName = majorName

    def includesCourse(self, db, course_code):
        """Xác định học phần có thuộc chương trình đào tạo của ngành hay không."""
        curriculum_entry = db.fetch_one(
            "select 1 from curriculum where major_code=%s and course_code=%s",
            (self.majorCode, course_code),
        )
        if curriculum_entry:
            return True
        return False
