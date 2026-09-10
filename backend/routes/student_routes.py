"""Student API: receives HTTP requests and calls business objects while preserving the frontend contract."""

from flask import Blueprint, request
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from services.registration_service import Student

student_bp = Blueprint("student", __name__, url_prefix="/api/student")


@student_bp.get("/profile")
@require_auth("student")
def profile():
    """Read the profile for the current account without allowing access to another user’s profile."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewProfile()
    return api_response(result)


@student_bp.get("/semesters")
@require_auth("student")
def semesters():
    """Get the semester list so the user can select the data scope."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewSemesters()
    return api_response(result)


@student_bp.get("/registration-periods")
@require_auth("student")
def registration_periods():
    """Get registration periods with status calculated from the current date."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewRegistrationPeriods()
    return api_response(result)


@student_bp.get("/curriculum")
@require_auth("student")
def curriculum():
    """Get the curriculum for the current student’s major."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewCurriculum()
    return api_response(result)


@student_bp.get("/courses")
@require_auth("student")
def courses():
    """Look up courses in the major together with prerequisites and available seats."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewCourses(query=query)
    return api_response(result)


@student_bp.post("/registrations")
@require_auth("student")
def register_course():
    """Validate conditions, then save the registration in a transaction with locking to prevent capacity overflow."""
    current_user = get_current_user()
    student = Student(current_user)
    data = read_json_object()

    result = student.registerCourse(data=data)
    return api_response(result)


@student_bp.get("/registrations")
@require_auth("student")
def registrations():
    """View the current student’s registrations and statuses by semester."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewRegistrationStatus(query=query)
    return api_response(result)


@student_bp.put("/registrations/<registration_id>/drop")
@require_auth("student")
def drop_course(registration_id):
    """Drop the current student’s registration while the registration period is still open."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.dropCourse(registration_id)
    return api_response(result)


@student_bp.get("/grades")
@require_auth("student")
def grades():
    """View the current student’s grades and results by semester."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewGrades(query=query)
    return api_response(result)
