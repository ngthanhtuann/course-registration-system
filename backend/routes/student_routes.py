"""API routes for Student functions."""

from flask import Blueprint, request
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from models.student import Student
student_bp = Blueprint("student", __name__, url_prefix="/api/student")


@student_bp.get("/profile")
@require_auth("student")
def profile():
    """Get the current student profile."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewProfile()
    return api_response(result)


@student_bp.get("/semesters")
@require_auth("student")
def semesters():
    """Get all semesters."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewSemesters()
    return api_response(result)


@student_bp.get("/registration-periods")
@require_auth("student")
def registration_periods():
    """Get registration periods."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewRegistrationPeriods()
    return api_response(result)


@student_bp.get("/curriculum")
@require_auth("student")
def curriculum():
    """Get the student curriculum."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.viewCurriculum()
    return api_response(result)


@student_bp.get("/courses")
@require_auth("student")
def courses():
    """Get courses available to the student."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewCourses(query=query)
    return api_response(result)


@student_bp.post("/registrations")
@require_auth("student")
def register_course():
    """Register the student for a course."""
    current_user = get_current_user()
    student = Student(current_user)
    data = read_json_object()

    result = student.registerCourse(data=data)
    return api_response(result)


@student_bp.get("/registrations")
@require_auth("student")
def registrations():
    """Get the student registration status."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewRegistrationStatus(query=query)
    return api_response(result)


@student_bp.put("/registrations/<registration_id>/drop")
@require_auth("student")
def drop_course(registration_id):
    """Drop a registered course."""
    current_user = get_current_user()
    student = Student(current_user)

    result = student.dropCourse(registration_id)
    return api_response(result)


@student_bp.get("/grades")
@require_auth("student")
def grades():
    """Get the student grades."""
    current_user = get_current_user()
    student = Student(current_user)
    query = request.args.to_dict()

    result = student.viewGrades(query=query)
    return api_response(result)
