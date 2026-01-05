from functools import wraps
from flask import request, jsonify

from utils.auth import decode_token


def token_required(required_role=None):
    """
    Middleware to protect routes using JWT
    Optionally enforce role-based access
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # ✅ ALLOW CORS PREFLIGHT REQUESTS
            if request.method == "OPTIONS":
                return jsonify({}), 200

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization token missing"}), 401

            token = auth_header.split(" ")[1]
            decoded = decode_token(token)

            if not decoded:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Role check (if required)
            if required_role and decoded.get("role") != required_role:
                return jsonify({"error": "Insufficient permissions"}), 403

            # Attach user info to request context
            request.user = {
                "id": decoded["user_id"],
                "role": decoded["role"]
            }

            return f(*args, **kwargs)

        return wrapper

    return decorator
