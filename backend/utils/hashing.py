import hashlib


def generate_image_hash(image_bytes: bytes) -> str:
    """
    Generate SHA256 hash of image bytes
    """
    sha256 = hashlib.sha256()
    sha256.update(image_bytes)
    return sha256.hexdigest()
