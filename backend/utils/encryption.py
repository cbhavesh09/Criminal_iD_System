import os
import base64


def generate_key(length: int = 16) -> bytes:
    """
    Generate random encryption key
    """
    return os.urandom(length)


def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """
    XOR encrypt/decrypt data using key
    """
    return bytes(
        data[i] ^ key[i % len(key)]
        for i in range(len(data))
    )


def encrypt_image(image_bytes: bytes):
    """
    Encrypt image bytes and return base64 encoded data + key
    """
    key = generate_key()
    encrypted_bytes = xor_encrypt_decrypt(image_bytes, key)

    return {
        "encrypted_image": base64.b64encode(encrypted_bytes).decode("utf-8"),
        "key": base64.b64encode(key).decode("utf-8")
    }


def decrypt_image(encrypted_base64: str, key_base64: str) -> bytes:
    """
    Decrypt base64 encrypted image using base64 key
    """
    encrypted_bytes = base64.b64decode(encrypted_base64)
    key = base64.b64decode(key_base64)

    return xor_encrypt_decrypt(encrypted_bytes, key)
