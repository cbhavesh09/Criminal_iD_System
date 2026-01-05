from datetime import datetime
from bson import ObjectId
from config import db

print("🔥 LOADING NEW CriminalModel WITHOUT case_number 🔥")


class CriminalModel:
    collection = db.criminals

    @classmethod
    def generate_case_number(cls):
        count = cls.collection.count_documents({})
        return f"CASE-{str(count + 1).zfill(6)}"

    @classmethod
    def create_criminal(
        cls,
        image_hash,
        encrypted_image,
        encryption_key,
        name,
        age,
        charges,
        uploaded_by
    ):
        existing = cls.collection.find_one({"imageHash": image_hash})
        if existing:
            return None

        case_number = cls.generate_case_number()

        criminal_data = {
            "imageHash": image_hash,
            "encryptedImage": encrypted_image,
            "encryptionKey": encryption_key,
            "name": name,
            "caseNumber": case_number,
            "age": age,
            "charges": charges,
            "uploadedBy": uploaded_by,
            "status": "active",
            "createdAt": datetime.utcnow()
        }

        result = cls.collection.insert_one(criminal_data)
        criminal_data["_id"] = result.inserted_id
        return criminal_data

    @classmethod
    def find_all(cls):
        return list(cls.collection.find({}))

    @classmethod
    def find_by_hash(cls, image_hash):
        return cls.collection.find_one({"imageHash": image_hash})

    @classmethod
    def find_by_id(cls, criminal_id):
        try:
            return cls.collection.find_one({"_id": ObjectId(criminal_id)})
        except Exception:
            return None
