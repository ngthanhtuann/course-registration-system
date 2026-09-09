"""Chuyển đổi dữ liệu tại biên HTTP; lớp nghiệp vụ không import Flask."""

from datetime import date
from flask import jsonify, request
from flask.json.provider import DefaultJSONProvider
from werkzeug.exceptions import BadRequest


def read_json_object():
    """Nhận JSON object; từ chối mảng/chuỗi để tránh lỗi gọi .get trên dữ liệu sai kiểu."""
    data = request.get_json()
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise BadRequest("JSON body must be an object")
    return data


def api_response(result):
    """Đổi kết quả nghiệp vụ thành JSON và giữ mã HTTP của các API hiện tại."""
    if isinstance(result, tuple):
        payload, status = result
        return jsonify(payload), status
    return jsonify(result)


class ISOJSONProvider(DefaultJSONProvider):
    """Serialize database dates as ISO values accepted by frontend date inputs."""

    @staticmethod
    def default(value):
        """Preserve Flask serialization except for date and datetime values."""
        if isinstance(value, date):
            return value.isoformat()
        return DefaultJSONProvider.default(value)
