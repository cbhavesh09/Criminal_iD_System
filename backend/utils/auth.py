
import jwt
from datetime import datetime, timedelta
from config import Config


def generate_token(user_id: str, role: str):
    """
    Generate JWT token
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token


def decode_token(token: str):
    """
    Decode JWT token
    """
    try:
        decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
