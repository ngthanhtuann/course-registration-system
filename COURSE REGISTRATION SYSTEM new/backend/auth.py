"""API User: nhận HTTP và gọi đối tượng nghiệp vụ, giữ nguyên hợp đồng frontend."""

from flask import Blueprint
from security import require_auth, get_current_user
from http_support import api_response, read_json_object
from domain.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.post("/login")
def login():
    """Xác thực tài khoản đang hoạt động và cấp token đăng nhập."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.login(data=data)
    return api_response(result)


@auth_bp.get("/me")
@require_auth()
def me():
    """Đọc thông tin tài khoản của người dùng hiện tại."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.viewAccountInfo()
    return api_response(result)


@auth_bp.put("/account/profile")
@require_auth()
def update_profile():
    """Cập nhật họ tên, email và kiểm tra email bị trùng."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.updateProfile(data=data)
    return api_response(result)


@auth_bp.put("/account/password")
@require_auth()
def change_password():
    """Kiểm tra mật khẩu cũ rồi lưu mật khẩu mới dưới dạng băm."""
    current_user = get_current_user()
    account = User(current_user)
    data = read_json_object()

    result = account.changePassword(data=data)
    return api_response(result)


@auth_bp.post("/logout")
@require_auth()
def logout():
    """Trả xác nhận đăng xuất; client phải xóa JWT đang lưu để kết thúc phiên."""
    current_user = get_current_user()
    account = User(current_user)

    result = account.logout()
    return api_response(result)
