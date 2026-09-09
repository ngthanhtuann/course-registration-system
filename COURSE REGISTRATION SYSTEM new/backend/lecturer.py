"""API Lecturer: nhận HTTP và gọi đối tượng nghiệp vụ, giữ nguyên hợp đồng frontend."""

from flask import Blueprint, request
from security import require_auth, get_current_user
from http_support import api_response, read_json_object
from domain.lecturer import Lecturer

lecturer_bp = Blueprint("lecturer", __name__, url_prefix="/api/lecturer")


@lecturer_bp.get("/profile")
@require_auth("lecturer")
def profile():
    """Đọc hồ sơ theo tài khoản hiện tại, không cho truy cập hồ sơ người khác."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)

    result = lecturer.viewProfile()
    return api_response(result)


@lecturer_bp.get("/semesters")
@require_auth("lecturer")
def semesters():
    """Lấy danh sách học kỳ để người dùng chọn phạm vi dữ liệu."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)

    result = lecturer.viewSemesters()
    return api_response(result)


@lecturer_bp.get("/teaching-courses")
@require_auth("lecturer")
def teaching_courses():
    """Lấy các học phần được phân công cho giảng viên trong học kỳ."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    query = request.args.to_dict()

    result = lecturer.viewTeachingCourse(query=query)
    return api_response(result)


@lecturer_bp.get("/courses/<course_code>/students")
@require_auth("lecturer")
def course_students(course_code):
    """Kiểm tra phân công trước khi lấy danh sách sinh viên đăng ký."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    query = request.args.to_dict()

    result = lecturer.viewRegisteredStudents(course_code, query=query)
    return api_response(result)


@lecturer_bp.put("/registrations/<registration_id>/grade")
@require_auth("lecturer")
def update_grade(registration_id):
    """Kiểm tra phân công, thời hạn và điểm trước khi cập nhật kết quả."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    data = read_json_object()

    result = lecturer.manageStudentGrade(registration_id, data=data)
    return api_response(result)
