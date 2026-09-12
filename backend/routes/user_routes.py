"""API routes for Administrator functions."""

import csv
from io import StringIO

from flask import Blueprint, Response, request
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from models.admin import Administrator
admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/dashboard")
@require_auth("admin")
def dashboard():
    """Get information for the Admin dashboard."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.dashboard()
    return api_response(result)


@admin_bp.get("/users")
@require_auth("admin")
def list_users():
    """Get all users."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.list_users()
    return api_response(result)


@admin_bp.post("/users")
@require_auth("admin")
def create_user():
    """Create a Student or Lecturer account."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_user(data=data)
    return api_response(result)


@admin_bp.put("/users/<user_id>")
@require_auth("admin")
def update_user(user_id):
    """Update a user account."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_user(user_id, data=data)
    return api_response(result)


@admin_bp.delete("/users/<user_id>")
@require_auth("admin")
def deactivate_user(user_id):
    """Deactivate a user account."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.deactivate_user(user_id)
    return api_response(result)


@admin_bp.get("/majors")
@require_auth("admin")
def list_majors():
    """Get all majors."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageMajor()
    return api_response(result)


@admin_bp.post("/majors")
@require_auth("admin")
def create_major():
    """Create a major."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_major(data=data)
    return api_response(result)


@admin_bp.put("/majors/<major_code>")
@require_auth("admin")
def update_major(major_code):
    """Update a major."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_major(major_code, data=data)
    return api_response(result)


@admin_bp.delete("/majors/<major_code>")
@require_auth("admin")
def delete_major(major_code):
    """Delete a major."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_major(major_code)
    return api_response(result)


@admin_bp.get("/courses")
@require_auth("admin")
def list_courses():
    """Get all courses."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageCourse()
    return api_response(result)


@admin_bp.post("/courses")
@require_auth("admin")
def create_course():
    """Create a course."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_course(data=data)
    return api_response(result)


@admin_bp.put("/courses/<course_code>")
@require_auth("admin")
def update_course(course_code):
    """Update a course."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_course(course_code, data=data)
    return api_response(result)


@admin_bp.delete("/courses/<course_code>")
@require_auth("admin")
def delete_course(course_code):
    """Delete a course."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_course(course_code)
    return api_response(result)


@admin_bp.get("/curriculum/<major_code>")
@require_auth("admin")
def get_curriculum(major_code):
    """Get a major curriculum."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageCurriculum(major_code)
    return api_response(result)


@admin_bp.post("/curriculum")
@require_auth("admin")
def add_curriculum():
    """Add a course to a curriculum."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.add_curriculum(data=data)
    return api_response(result)


@admin_bp.put("/curriculum/<curriculum_id>")
@require_auth("admin")
def update_curriculum(curriculum_id):
    """Update a curriculum item."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_curriculum(curriculum_id, data=data)
    return api_response(result)


@admin_bp.delete("/curriculum/<curriculum_id>")
@require_auth("admin")
def remove_curriculum(curriculum_id):
    """Remove a course from a curriculum."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.remove_curriculum(curriculum_id)
    return api_response(result)


@admin_bp.get("/semesters")
@require_auth("admin")
def list_semesters():
    """Get all semesters."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageSemester()
    return api_response(result)


@admin_bp.post("/semesters")
@require_auth("admin")
def create_semester():
    """Create a semester."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_semester(data=data)
    return api_response(result)


@admin_bp.put("/semesters/<semester_id>")
@require_auth("admin")
def update_semester(semester_id):
    """Update a semester."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_semester(semester_id, data=data)
    return api_response(result)


@admin_bp.delete("/semesters/<semester_id>")
@require_auth("admin")
def delete_semester(semester_id):
    """Delete a semester."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_semester(semester_id)
    return api_response(result)


@admin_bp.get("/registration-periods")
@require_auth("admin")
def list_periods():
    """Get all registration periods."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.manageRegistrationPeriod()
    return api_response(result)


@admin_bp.post("/registration-periods")
@require_auth("admin")
def create_period():
    """Create a registration period."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.create_period(data=data)
    return api_response(result)


@admin_bp.put("/registration-periods/<period_id>")
@require_auth("admin")
def update_period(period_id):
    """Update a registration period."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.update_period(period_id, data=data)
    return api_response(result)


@admin_bp.delete("/registration-periods/<period_id>")
@require_auth("admin")
def delete_period(period_id):
    """Delete a registration period."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_period(period_id)
    return api_response(result)


@admin_bp.get("/registration-demand")
@admin_bp.get("/registration-demand/report")
@require_auth("admin")
def registration_demand():
    """Aggregate registration demand by registration period and major."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.generateRegistrationDemandReport(query=query)
    if isinstance(result, tuple):
        return api_response(result)
    if request.path.endswith("/report") or query.get("format") == "csv":
        output = StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(["Course Code", "Course Name", "Credit", "Capacity", "Registered Students"])
        for row in result:
            cells = []
            for field in ("course_code", "course_name", "credit", "max_capacity", "registered_students"):
                value = row[field]
                if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
                    value = "'" + value
                cells.append(value)
            writer.writerow(cells)
        return Response(
            "\ufeff" + output.getvalue(),
            content_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": 'attachment; filename="registration-demand.csv"'},
        )
    return api_response(result)


@admin_bp.get("/registration-demand/<course_code>/students")
@require_auth("admin")
def demand_students(course_code):
    """Get students in the demand report for the selected course."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.demand_students(course_code, query=query)
    return api_response(result)


@admin_bp.get("/teaching-assignments")
@require_auth("admin")
def list_assignments():
    """List teaching assignments and handle related data constraints."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    query = request.args.to_dict()

    result = administrator.list_assignments(query=query)
    return api_response(result)


@admin_bp.delete("/teaching-assignments/<assignment_id>")
@require_auth("admin")
def delete_assignment(assignment_id):
    """Delete a teaching assignment and handle related data constraints."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.delete_assignment(assignment_id)
    return api_response(result)


@admin_bp.get("/qualified-lecturers/<course_code>")
@require_auth("admin")
def qualified_lecturers(course_code):
    """List lecturers whose qualifications match the course."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.qualified_lecturers(course_code)
    return api_response(result)


@admin_bp.post("/lecturer-qualifications")
@require_auth("admin")
def add_qualification():
    """Add a lecturer qualification and handle related data constraints."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.add_qualification(data=data)
    return api_response(result)


@admin_bp.delete("/lecturer-qualifications/<lecturer_id>/<course_code>")
@require_auth("admin")
def remove_qualification(lecturer_id, course_code):
    """Remove a lecturer qualification and handle related data constraints."""
    current_user = get_current_user()
    administrator = Administrator(current_user)

    result = administrator.remove_qualification(lecturer_id, course_code)
    return api_response(result)


@admin_bp.post("/teaching-assignments")
@require_auth("admin")
def assign_lecturer():
    """Verify qualifications, then save the lecturer assignment for the semester."""
    current_user = get_current_user()
    administrator = Administrator(current_user)
    data = read_json_object()

    result = administrator.assignLecturer(data=data)
    return api_response(result)
