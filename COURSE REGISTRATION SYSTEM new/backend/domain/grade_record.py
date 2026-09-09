"""Bản ghi điểm được ánh xạ vào các cột grade/result_status của registrations."""

from math import isfinite


class GradeRecord:
    """Đóng gói điểm và kết quả; một đăng ký có thể chưa có bản ghi điểm."""

    def __init__(self, grade=None, resultStatus=None):
        """Lưu điểm và kết quả; None nghĩa là chưa có dữ liệu."""
        self.grade = grade
        self.resultStatus = resultStatus

    def calculateResultStatus(self):
        """Kiểm tra điểm hữu hạn trong 0–10; điểm từ 5 là đạt, chưa nhập trả None."""
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
