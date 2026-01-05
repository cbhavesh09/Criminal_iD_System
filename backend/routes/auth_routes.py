from flask import Blueprint, request, jsonify

from models.user import UserModel
from utils.auth import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ================================
# SIGNUP
# ================================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    required_fields = ["name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = UserModel.create_user(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data.get("role", "officer")
    )

    if not user:
        return jsonify({"error": "User already exists"}), 409

    return jsonify({
        "message": "User created successfully"
    }), 201


# ================================
# LOGIN (RETURNS JWT TOKEN)
# ================================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    user = UserModel.find_by_email(data["email"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not UserModel.verify_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🔐 Generate JWT token
    token = generate_token(
        user_id=str(user["_id"]),
        role=user["role"]
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200
