import re
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import UPLOAD_FOLDER
from app.utils.logger import logger


def sanitize_filename(filename: str) -> str:

    filename = Path(filename).name
    filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
    return filename


def create_upload_directory() -> Path:

    upload_path = Path(UPLOAD_FOLDER)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def generate_unique_filename(filename: str) -> str:

    safe_filename = sanitize_filename(filename)
    return f"{uuid.uuid4().hex}_{safe_filename}"


def check_file_exists(
    file_path: Path
) -> Path:

    if not file_path.exists():

        logger.error(
            f"File not found: {file_path}"
        )

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return file_path


def save_uploaded_file(file: UploadFile) -> dict:

    upload_path = create_upload_directory()

    file_uuid = uuid.uuid4()
    safe_filename = sanitize_filename(file.filename)
    unique_name = f"{file_uuid.hex}_{safe_filename}"

    destination = upload_path / unique_name

    logger.info(f"Saving file: {unique_name}")

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File successfully saved: {destination}")

        return {
            "file_id": str(file_uuid),
            "stored_filename": unique_name,
            "path": destination,
        }

    except Exception as error:
        logger.error(f"Error while saving file: {error}")
        raise
