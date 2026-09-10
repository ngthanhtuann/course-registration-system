"""User API: receives HTTP requests and calls business objects while preserving the frontend contract."""

from flask import Blueprint
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from services.auth_service import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.post("/login")
def login():
    """Authenticate an active account and issue a login token."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.login(data=data)
    return api_response(result)


@auth_bp.get("/me")
@require_auth()
def me():
    """Read the current user’s account information."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.viewAccountInfo()
    return api_response(result)


@auth_bp.put("/account/profile")
@require_auth()
def update_profile():
    """Update full name and email, and check for duplicate email addresses."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.updateProfile(data=data)
    return api_response(result)


@auth_bp.put("/account/password")
@require_auth()
def change_password():
    """Verify the old password, then store the new password as a hash."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.changePassword(data=data)
    return api_response(result)


@auth_bp.post("/logout")
@require_auth()
def logout():
    """Return logout confirmation; the client must delete the stored JWT to end the session."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.logout()
    return api_response(result)
