"""API Administrator: nhận HTTP và gọi đối tượng nghiệp vụ, giữ nguyên hợp đồng frontend."""

from flask import Blueprint, request
from security import require_auth, get_current_user
from http_support import api_response, read_json_object
from domain.administrator import Administrator

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
@require_auth("admin")
def dashboard():
    """Tổng hợp số liệu người dùng, học phần và đăng ký cho trang quản trị."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.dashboard()
    return api_response(result)


@admin_bp.get("/users")
@require_auth("admin")
def list_users():
    """Liệt kê người dùng và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.list_users()
    return api_response(result)


@admin_bp.post("/users")
@require_auth("admin")
def create_user():
    """Tạo người dùng và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_user(data=data)
    return api_response(result)


@admin_bp.put("/users/<user_id>")
@require_auth("admin")
def update_user(user_id):
    """Cập nhật người dùng và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_user(user_id, data=data)
    return api_response(result)


@admin_bp.delete("/users/<user_id>")
@require_auth("admin")
def deactivate_user(user_id):
    """Vô hiệu hóa người dùng và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.deactivate_user(user_id)
    return api_response(result)


@admin_bp.get("/majors")
@require_auth("admin")
def list_majors():
    """Liệt kê ngành học và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageMajor()
    return api_response(result)


@admin_bp.post("/majors")
@require_auth("admin")
def create_major():
    """Tạo ngành học và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_major(data=data)
    return api_response(result)


@admin_bp.put("/majors/<major_code>")
@require_auth("admin")
def update_major(major_code):
    """Cập nhật ngành học và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_major(major_code, data=data)
    return api_response(result)


@admin_bp.delete("/majors/<major_code>")
@require_auth("admin")
def delete_major(major_code):
    """Xóa ngành học và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_major(major_code)
    return api_response(result)


@admin_bp.get("/courses")
@require_auth("admin")
def list_courses():
    """Liệt kê học phần và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageCourse()
    return api_response(result)


@admin_bp.post("/courses")
@require_auth("admin")
def create_course():
    """Tạo học phần và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_course(data=data)
    return api_response(result)


@admin_bp.put("/courses/<course_code>")
@require_auth("admin")
def update_course(course_code):
    """Cập nhật học phần và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_course(course_code, data=data)
    return api_response(result)


@admin_bp.delete("/courses/<course_code>")
@require_auth("admin")
def delete_course(course_code):
    """Xóa học phần và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_course(course_code)
    return api_response(result)


@admin_bp.get("/curriculum/<major_code>")
@require_auth("admin")
def get_curriculum(major_code):
    """Đọc mục chương trình đào tạo và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageCurriculum(major_code)
    return api_response(result)


@admin_bp.post("/curriculum")
@require_auth("admin")
def add_curriculum():
    """Thêm mục chương trình đào tạo và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.add_curriculum(data=data)
    return api_response(result)


@admin_bp.put("/curriculum/<curriculum_id>")
@require_auth("admin")
def update_curriculum(curriculum_id):
    """Cập nhật mục chương trình đào tạo và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_curriculum(curriculum_id, data=data)
    return api_response(result)


@admin_bp.delete("/curriculum/<curriculum_id>")
@require_auth("admin")
def remove_curriculum(curriculum_id):
    """Gỡ mục chương trình đào tạo và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.remove_curriculum(curriculum_id)
    return api_response(result)


@admin_bp.get("/semesters")
@require_auth("admin")
def list_semesters():
    """Liệt kê học kỳ và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageSemester()
    return api_response(result)


@admin_bp.post("/semesters")
@require_auth("admin")
def create_semester():
    """Tạo học kỳ và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_semester(data=data)
    return api_response(result)


@admin_bp.put("/semesters/<semester_id>")
@require_auth("admin")
def update_semester(semester_id):
    """Cập nhật học kỳ và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_semester(semester_id, data=data)
    return api_response(result)


@admin_bp.delete("/semesters/<semester_id>")
@require_auth("admin")
def delete_semester(semester_id):
    """Xóa học kỳ và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_semester(semester_id)
    return api_response(result)


@admin_bp.get("/registration-periods")
@require_auth("admin")
def list_periods():
    """Liệt kê đợt đăng ký và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageRegistrationPeriod()
    return api_response(result)


@admin_bp.post("/registration-periods")
@require_auth("admin")
def create_period():
    """Tạo đợt đăng ký và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_period(data=data)
    return api_response(result)


@admin_bp.put("/registration-periods/<period_id>")
@require_auth("admin")
def update_period(period_id):
    """Cập nhật đợt đăng ký và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_period(period_id, data=data)
    return api_response(result)


@admin_bp.delete("/registration-periods/<period_id>")
@require_auth("admin")
def delete_period(period_id):
    """Xóa đợt đăng ký và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_period(period_id)
    return api_response(result)


@admin_bp.get("/registration-demand")
@require_auth("admin")
def registration_demand():
    """Tổng hợp nhu cầu đăng ký theo đợt và ngành học."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.generateRegistrationDemandReport(query=query)
    return api_response(result)


@admin_bp.get("/registration-demand/<course_code>/students")
@require_auth("admin")
def demand_students(course_code):
    """Lấy sinh viên trong báo cáo nhu cầu của học phần được chọn."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.demand_students(course_code, query=query)
    return api_response(result)


@admin_bp.get("/teaching-assignments")
@require_auth("admin")
def list_assignments():
    """Liệt kê phân công giảng dạy và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.list_assignments(query=query)
    return api_response(result)


@admin_bp.delete("/teaching-assignments/<assignment_id>")
@require_auth("admin")
def delete_assignment(assignment_id):
    """Xóa phân công giảng dạy và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_assignment(assignment_id)
    return api_response(result)


@admin_bp.get("/qualified-lecturers/<course_code>")
@require_auth("admin")
def qualified_lecturers(course_code):
    """Liệt kê giảng viên có chuyên môn phù hợp với học phần."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.qualified_lecturers(course_code)
    return api_response(result)


@admin_bp.post("/lecturer-qualifications")
@require_auth("admin")
def add_qualification():
    """Thêm chuyên môn giảng viên và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.add_qualification(data=data)
    return api_response(result)


@admin_bp.delete("/lecturer-qualifications/<lecturer_id>/<course_code>")
@require_auth("admin")
def remove_qualification(lecturer_id, course_code):
    """Gỡ chuyên môn giảng viên và xử lý ràng buộc dữ liệu liên quan."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.remove_qualification(lecturer_id, course_code)
    return api_response(result)


@admin_bp.post("/teaching-assignments")
@require_auth("admin")
def assign_lecturer():
    """Kiểm tra chuyên môn rồi lưu phân công giảng viên cho học kỳ."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.assignLecturer(data=data)
    return api_response(result)
