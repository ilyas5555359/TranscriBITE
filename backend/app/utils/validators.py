from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import MAX_FILE_SIZE

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
}

ALLOWED_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/flac",
    "audio/aac",
    "audio/ogg",
    "video/mp4",
    "video/x-msvideo",
    "video/quicktime",
    "video/x-matroska"
}

def validate_uploaded_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file extension."
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    max_size = MAX_FILE_SIZE * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
        status_code=400,
        detail=f"File exceeds the maximum size of {MAX_FILE_SIZE} MB."
    )