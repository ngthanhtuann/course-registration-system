"""Registration object linking a student, course, registration period, and grade."""

from uuid import uuid4


class Registration:
    """Store a student’s course registration and grade information."""

    def __init__(
        self,
        studentId,
        courseCode,
        periodId,
        registrationId=None,
        registrationStatus="registered",
        gradeRecord=None,
    ):
        """Create a registration linking the student, course, registration period, and grade if available."""
        self.studentId = studentId
        self.courseCode = courseCode
        self.periodId = periodId
        self.registrationId = registrationId
        self.registrationStatus = registrationStatus
        self.gradeRecord = gradeRecord

    def saveRegistration(self, db):
        """Create or reactivate a dropped registration within a transaction managed by the caller."""
        existing = db.fetch_one(
            'select registration_id from registrations where student_id=%s and period_id=%s and course_id=(select course_id from courses where course_code=%s)',
            (self.studentId, self.periodId, self.courseCode),
        )
        if existing:
            self.registrationId = existing["registration_id"]
            db.execute(
                "update registrations set status='REGISTERED', "
                "grade=null, result_status=null where registration_id=%s",
                (self.registrationId,),
            )
        else:
            if not self.registrationId:
                self.registrationId = uuid4().hex
            # The registration_id column in the database allows at most 20 characters.
            self.registrationId = self.registrationId[:20]
            db.execute(
                "insert into registrations "
                "(registration_id, student_id, course_id, semester_id, status, period_id) "
                "values (%s, %s, (select course_id from courses where course_code=%s), "
                "(select semester_id from registration_periods where period_id=%s), "
                "'REGISTERED', %s)",
                (
                    self.registrationId,
                    self.studentId,
                    self.courseCode,
                    self.periodId,
                    self.periodId,
                ),
            )
        self.registrationStatus = "registered"
        self.gradeRecord = None
        return self.registrationId

    def updateRegistrationStatus(self, db, status):
        """Update to a valid status; the caller checks ownership and deadlines first."""
        if status not in ("registered", "dropped"):
            raise ValueError("invalid registration status")
        db.execute(
            "update registrations set status=%s where registration_id=%s",
            (status.upper(), self.registrationId),
        )
        self.registrationStatus = status
