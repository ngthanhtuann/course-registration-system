"""Grade model."""

from math import isfinite


class GradeRecord:
    """Store a grade and its result status."""

    def __init__(self, grade=None, resultStatus=None):
        """Create a GradeRecord object."""
        self.grade = grade
        self.resultStatus = resultStatus

    def calculateResultStatus(self):
        """Check the grade and return passed or failed."""
        if self.grade is None:
            self.resultStatus = None
        else:
            if not isfinite(self.grade) or not 0 <= self.grade <= 10:
                raise ValueError("grade must be between 0 and 10")
            if self.grade >= 5:
                self.resultStatus = "passed"
            else:
                self.resultStatus = "not passed"
        return self.resultStatus
