"""Transform data at the HTTP boundary; the business layer does not import Flask."""

from datetime import date
from flask import jsonify, request
from flask.json.provider import DefaultJSONProvider
from werkzeug.exceptions import BadRequest


def read_json_object():
    """Accept a JSON object; reject arrays/strings to avoid calling .get on incorrectly typed data."""
    data = request.get_json()
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise BadRequest("JSON body must be an object")
    return data


def api_response(result):
    """Convert business results to JSON while preserving the HTTP status codes of the current APIs."""
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
