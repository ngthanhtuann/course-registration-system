"""Grade model."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class GradeRecord:
    """Store a normalized grade and its result status."""

    def __init__(self, grade=None, resultStatus=None):
        """Create a GradeRecord object."""
        self.grade = self.normalizeGrade(grade)
        self.resultStatus = resultStatus

    @staticmethod
    def normalizeGrade(grade):
        """Validate a grade and round it to two decimal places."""
        if grade is None:
            return None

        try:
            value = Decimal(str(grade))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("grade must be a number")

        if not value.is_finite() or value < Decimal("0") or value > Decimal("10"):
            raise ValueError("grade must be between 0 and 10")

        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculateResultStatus(self):
        """Return passed or not passed from the normalized grade."""
        if self.grade is None:
            self.resultStatus = None
        elif self.grade >= Decimal("5.00"):
            self.resultStatus = "passed"
        else:
            self.resultStatus = "not passed"

        return self.resultStatus
