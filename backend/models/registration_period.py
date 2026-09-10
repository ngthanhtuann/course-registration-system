"""A registration period belongs to a semester; its status is derived from the start/end dates."""

from datetime import date, datetime


class RegistrationPeriod:
    """Store registration-period information; status is calculated from the current date."""

    def __init__(
        self,
        periodName,
        startDate,
        endDate,
        periodId=None,
        semesterId=None,
        registrationStatus="upcoming",
    ):
        """Create a registration period with its dates, semester, and initial status."""
        self.periodName = periodName
        self.startDate = startDate.date() if isinstance(startDate, datetime) else startDate
        self.endDate = endDate.date() if isinstance(endDate, datetime) else endDate
        self.periodId = periodId
        self.semesterId = semesterId
        self.registrationStatus = registrationStatus

    def updateRegistrationStatus(self, today=None):
        """Update and return upcoming/open/closed status; both boundary dates are inclusive."""
        if not today:
            today = date.today()

        if isinstance(today, datetime):
            today = today.date()
        if today < self.startDate:
            self.registrationStatus = "upcoming"
        elif today <= self.endDate:
            self.registrationStatus = "open"
        else:
            self.registrationStatus = "closed"
        return self.registrationStatus
