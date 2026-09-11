"""API routes for login and account management."""

from flask import Blueprint
from utils.auth import require_auth, get_current_user
from utils.http_support import api_response, read_json_object
from models.user import User
auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.post("/login")
def login():
    """Log in and return a token."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.login(data=data)
    return api_response(result)


@auth_bp.get("/me")
@require_auth()
def me():
    """Get the current user account information."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.viewAccountInfo()
    return api_response(result)


@auth_bp.put("/account/profile")
@require_auth()
def update_profile():
    """Update the current user profile."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.updateProfile(data=data)
    return api_response(result)


@auth_bp.put("/account/password")
@require_auth()
def change_password():
    """Change the current user password."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.changePassword(data=data)
    return api_response(result)


@auth_bp.post("/logout")
@require_auth()
def logout():
    """Log out the current user."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.logout()
    return api_response(result)
