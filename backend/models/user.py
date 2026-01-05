from datetime import datetime
import bcrypt

from config import db


class UserModel:
    collection = db.users  # MongoDB collection

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Hash a plaintext password using bcrypt
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        """
        Verify plaintext password against hashed password
        """
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password
        )

    @classmethod
    def create_user(cls, name, email, password, role="officer"):
        """
        Create a new user account
        """
        existing_user = cls.collection.find_one({"email": email})
        if existing_user:
            return None  # User already exists

        user_data = {
            "name": name,
            "email": email,
            "password": cls.hash_password(password),
            "role": role,
            "createdAt": datetime.utcnow()
        }

        result = cls.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id

        return user_data

    @classmethod
    def find_by_email(cls, email):
        """
        Find user by email
        """
        return cls.collection.find_one({"email": email})

    @classmethod
    def find_by_id(cls, user_id):
        """
        Find user by ID
        """
        return cls.collection.find_one({"_id": user_id})
