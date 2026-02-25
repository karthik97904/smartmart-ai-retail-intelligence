import os

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_required_fields(data: dict, required: list) -> list:
    """Returns list of missing fields."""
    return [field for field in required if field not in data or data[field] is None]