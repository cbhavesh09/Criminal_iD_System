ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE_MB = 5


def validate_image_file(file):
    """
    Validate uploaded image file
    """
    if file is None:
        return False, "No file provided"

    if file.mimetype not in ALLOWED_IMAGE_TYPES:
        return False, "Invalid file type"

    file.seek(0, 2)  # move cursor to end
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, "File size exceeds limit"

    return True, None


def validate_required_fields(data: dict, required_fields: list):
    """
    Check required JSON fields
    """
    missing = [field for field in required_fields if field not in data]
    return missing
