from flask import Blueprint, request, jsonify
import base64

from models.criminal import CriminalModel
from utils.hashing import generate_image_hash
from utils.encryption import encrypt_image, decrypt_image
from utils.validators import validate_image_file
from middleware.auth_middleware import token_required
from flask_cors import cross_origin

criminal_bp = Blueprint("criminals", __name__, url_prefix="/api/criminals")


# ================================
# GET ALL CRIMINALS
# ================================
@criminal_bp.route("", methods=["GET", "OPTIONS"])
@cross_origin()
@token_required()
def get_all_criminals():
    criminals = CriminalModel.find_all()

    for criminal in criminals:
        criminal["_id"] = str(criminal["_id"])
        criminal.pop("encryptedImage", None)
        criminal.pop("encryptionKey", None)

    return jsonify(criminals), 200


# ================================
# ADD CRIMINAL (AUTO CASE NUMBER)
# ================================
@criminal_bp.route("", methods=["POST", "OPTIONS"])
@cross_origin()
@token_required()
def add_criminal():
    image_file = request.files.get("image")
    is_valid, error = validate_image_file(image_file)

    if not is_valid:
        return jsonify({"error": error}), 400

    image_bytes = image_file.read()
    image_hash = generate_image_hash(image_bytes)
    encrypted = encrypt_image(image_bytes)

    name = request.form.get("name")
    age = request.form.get("age")
    charges = request.form.get("charges")

    if not all([name, age, charges]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        age = int(age)
    except ValueError:
        return jsonify({"error": "Invalid age"}), 400

    charges_list = [c.strip() for c in charges.split(",") if c.strip()]

    criminal = CriminalModel.create_criminal(
        image_hash=image_hash,
        encrypted_image=encrypted["encrypted_image"],
        encryption_key=encrypted["key"],
        name=name.strip(),
        age=age,
        charges=charges_list,
        uploaded_by=request.user["id"]
    )

    if not criminal:
        return jsonify({"error": "Criminal already exists"}), 409

    criminal["_id"] = str(criminal["_id"])

    return jsonify({
        "message": "Criminal added successfully",
        "criminal": criminal
    }), 201


# ================================
# DECRYPT IMAGE
# ================================
@criminal_bp.route("/<criminal_id>/decrypt-image", methods=["GET", "OPTIONS"])
@cross_origin()
@token_required()
def decrypt_criminal_image(criminal_id):
    criminal = CriminalModel.find_by_id(criminal_id)

    if not criminal:
        return jsonify({"error": "Criminal not found"}), 404

    decrypted_bytes = decrypt_image(
        encrypted_base64=criminal["encryptedImage"],
        key_base64=criminal["encryptionKey"]
    )

    image_base64 = base64.b64encode(decrypted_bytes).decode("utf-8")

    return jsonify({"image": image_base64}), 200
