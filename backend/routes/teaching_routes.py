"""Lecturer API: receives HTTP requests and calls business objects while preserving the frontend contract."""

from flask import Blueprint, request
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from services.grade_service import Lecturer

lecturer_bp = Blueprint("lecturer", __name__, url_prefix="/api/lecturer")


@lecturer_bp.get("/profile")
@require_auth("lecturer")
def profile():
    """Read the profile for the current account without allowing access to another user’s profile."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)

    result = lecturer.viewProfile()
    return api_response(result)


@lecturer_bp.get("/semesters")
@require_auth("lecturer")
def semesters():
    """Get the semester list so the user can select the data scope."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)

    result = lecturer.viewSemesters()
    return api_response(result)


@lecturer_bp.get("/teaching-courses")
@require_auth("lecturer")
def teaching_courses():
    """Get courses assigned to the lecturer for the semester."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    query = request.args.to_dict()

    result = lecturer.viewTeachingCourse(query=query)
    return api_response(result)


@lecturer_bp.get("/courses/<course_code>/students")
@require_auth("lecturer")
def course_students(course_code):
    """Verify the assignment before retrieving the list of registered students."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    query = request.args.to_dict()

    result = lecturer.viewRegisteredStudents(course_code, query=query)
    return api_response(result)


@lecturer_bp.put("/registrations/<registration_id>/grade")
@require_auth("lecturer")
def update_grade(registration_id):
    """Verify the assignment, deadline, and grade before updating the result."""
    current_user = get_current_user()
    lecturer = Lecturer(current_user)
    data = read_json_object()

    result = lecturer.manageStudentGrade(registration_id, data=data)
    return api_response(result)
