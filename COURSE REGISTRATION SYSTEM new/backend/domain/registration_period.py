"""Đợt đăng ký thuộc một học kỳ; trạng thái được suy ra từ ngày bắt đầu/kết thúc."""

from datetime import date, datetime


class RegistrationPeriod:
    """Lưu thông tin đợt đăng ký; trạng thái được tính theo ngày hiện tại."""

    def __init__(
        self,
        periodName,
        startDate,
        endDate,
        periodId=None,
        semesterId=None,
        registrationStatus="upcoming",
    ):
        """Tạo đợt đăng ký với thời gian, học kỳ và trạng thái ban đầu."""
        self.periodName = periodName
        self.startDate = startDate.date() if isinstance(startDate, datetime) else startDate
        self.endDate = endDate.date() if isinstance(endDate, datetime) else endDate
        self.periodId = periodId
        self.semesterId = semesterId
        self.registrationStatus = registrationStatus

    def updateRegistrationStatus(self, today=None):
        """Cập nhật và trả trạng thái upcoming/open/closed; cả hai ngày biên đều mở."""
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
