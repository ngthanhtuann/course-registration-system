"""The grade record maps to the grade/result_status columns of registrations."""

from math import isfinite


class GradeRecord:
    """Encapsulate grade and result; a registration may not yet have a grade record."""

    def __init__(self, grade=None, resultStatus=None):
        """Store grade and result; None means no data has been entered yet."""
        self.grade = grade
        self.resultStatus = resultStatus

    def calculateResultStatus(self):
        """Validate a finite grade from 0–10; grades of 5 or above pass, and an unentered grade returns None."""
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
