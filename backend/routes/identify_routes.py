from flask import Blueprint, request, jsonify

from models.criminal import CriminalModel
from utils.hashing import generate_image_hash
from utils.validators import validate_image_file
from middleware.auth_middleware import token_required

identify_bp = Blueprint("identify", __name__, url_prefix="/api/identify")


# ================================
# IDENTIFY SUSPECT BY IMAGE
# ================================
@identify_bp.route("", methods=["POST"])
@token_required()
def identify_criminal():
    """
    Accepts multipart/form-data:
    - image (file)
    """

    # ---------- Validate image ----------
    image_file = request.files.get("image")
    is_valid, error = validate_image_file(image_file)

    if not is_valid:
        return jsonify({"error": error}), 400

    # ---------- Read image bytes ----------
    image_bytes = image_file.read()

    # ---------- Generate SHA256 hash ----------
    image_hash = generate_image_hash(image_bytes)

    # ---------- Search in DB ----------
    criminal = CriminalModel.find_by_hash(image_hash)

    if not criminal:
        return jsonify({
            "match": False,
            "message": "No matching criminal found"
        }), 200

    # ---------- Prepare response ----------
    criminal["_id"] = str(criminal["_id"])

    # Do NOT expose encrypted image or key
    criminal.pop("encryptedImage", None)
    criminal.pop("encryptionKey", None)

    return jsonify({
        "match": True,
        "criminal": criminal
    }), 200
