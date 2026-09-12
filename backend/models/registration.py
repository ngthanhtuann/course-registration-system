"""Registration model."""

from uuid import uuid4


class Registration:
    """Store information about a student course registration."""

    def __init__(
        self,
        studentId,
        courseCode,
        periodId,
        registrationId=None,
        registrationStatus="registered",
        gradeRecord=None,
    ):
        """Create a Registration object."""
        self.studentId = studentId
        self.courseCode = courseCode
        self.periodId = periodId
        self.registrationId = registrationId
        self.registrationStatus = registrationStatus
        self.gradeRecord = gradeRecord

    def saveRegistration(self, db):
        """Save a new registration or reactivate a dropped one."""
        existing = db.fetch_one(
            "select registration_id from registrations where student_id=%s and semester_id=(select semester_id from registration_periods where period_id=%s) and course_code=%s",
            (self.studentId, self.periodId, self.courseCode),
        )
        if existing:
            self.registrationId = existing["registration_id"]
            db.execute(
                "update registrations set status='REGISTERED'::registration_status_type, period_id=%s, "
                "grade=null, result_status=null where registration_id=%s",
                (self.periodId, self.registrationId,),
            )
        else:
            if not self.registrationId:
                self.registrationId = uuid4().hex
            # registration_id can have at most 20 characters.
            self.registrationId = self.registrationId[:20]
            db.execute(
                "insert into registrations "
                "(registration_id, student_id, course_id, semester_id, status, period_id, course_code) "
                "values (%s, %s, (select course_id from courses where course_code=%s), "
                "(select semester_id from registration_periods where period_id=%s), "
                "'REGISTERED'::registration_status_type, %s, %s)",
                (
                    self.registrationId,
                    self.studentId,
                    self.courseCode,
                    self.periodId,
                    self.periodId,
                    self.courseCode,
                ),
            )
        self.registrationStatus = "registered"
        self.gradeRecord = None
        return self.registrationId

    def updateRegistrationStatus(self, db, status):
        """Update the registration status."""
        if status not in ("registered", "dropped"):
            raise ValueError("invalid registration status")
        db.execute(
            "update registrations set status=%s::registration_status_type where registration_id=%s",
            (status.upper(), self.registrationId),
        )
        self.registrationStatus = status
