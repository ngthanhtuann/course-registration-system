"""API Student: nhận HTTP và gọi đối tượng nghiệp vụ, giữ nguyên hợp đồng frontend."""

from flask import Blueprint, request
from security import require_auth, get_current_user
from http_support import api_response, read_json_object
from domain.student import Student

student_bp = Blueprint("student", __name__, url_prefix="/api/student")


@student_bp.get("/profile")
@require_auth("student")
def profile():
    """Đọc hồ sơ theo tài khoản hiện tại, không cho truy cập hồ sơ người khác."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewProfile()
    return api_response(result)


@student_bp.get("/semesters")
@require_auth("student")
def semesters():
    """Lấy danh sách học kỳ để người dùng chọn phạm vi dữ liệu."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewSemesters()
    return api_response(result)


@student_bp.get("/registration-periods")
@require_auth("student")
def registration_periods():
    """Lấy các đợt đăng ký kèm trạng thái tính theo ngày hiện tại."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewRegistrationPeriods()
    return api_response(result)


@student_bp.get("/curriculum")
@require_auth("student")
def curriculum():
    """Lấy chương trình đào tạo theo ngành của sinh viên hiện tại."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewCurriculum()
    return api_response(result)


@student_bp.get("/courses")
@require_auth("student")
def courses():
    """Tra cứu học phần thuộc ngành cùng điều kiện tiên quyết và chỗ trống."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewCourses(query=query)
    return api_response(result)


@student_bp.post("/registrations")
@require_auth("student")
def register_course():
    """Kiểm tra điều kiện rồi lưu đăng ký trong giao dịch có khóa chống vượt sĩ số."""
    current_user = get_current_user()
    student = Student(current_user)
    data = read_json_object()

    result = student.registerCourse(data=data)
    return api_response(result)


@student_bp.get("/registrations")
@require_auth("student")
def registrations():
    """Xem các đăng ký và trạng thái theo học kỳ của chính sinh viên."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewRegistrationStatus(query=query)
    return api_response(result)


@student_bp.put("/registrations/<registration_id>/drop")
@require_auth("student")
def drop_course(registration_id):
    """Hủy đăng ký thuộc sinh viên hiện tại khi đợt đăng ký còn mở."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.dropCourse(registration_id)
    return api_response(result)


@student_bp.get("/grades")
@require_auth("student")
def grades():
    """Xem điểm và kết quả của chính sinh viên theo học kỳ."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewGrades(query=query)
    return api_response(result)
