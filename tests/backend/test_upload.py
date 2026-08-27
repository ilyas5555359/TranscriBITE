from io import BytesIO
from pathlib import Path
from uuid import UUID

import pytest
from fastapi import HTTPException, UploadFile

from app.services import file_service as file_service_module
from app.services.file_service import (
    generate_unique_filename,
    sanitize_filename,
    save_uploaded_file,
)
from app.utils.validators import validate_uploaded_file


def _upload(filename="sample.wav", content_type="audio/wav", content=b"audio"):
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers={"content-type": content_type},
    )


def test_upload_success(tmp_path, monkeypatch):
    monkeypatch.setattr(file_service_module, "UPLOAD_FOLDER", str(tmp_path))
    file = _upload()

    result = save_uploaded_file(file)

    assert UUID(result["file_id"])
    assert Path(result["path"]).is_file()


def test_invalid_extension():
    with pytest.raises(HTTPException, match="Unsupported file extension"):
        validate_uploaded_file(_upload("sample.exe", "application/octet-stream"))


def test_invalid_mime_type():
    with pytest.raises(HTTPException, match="Unsupported file type"):
        validate_uploaded_file(_upload("sample.wav", "application/octet-stream"))


@pytest.mark.parametrize("filename, content_type", [
    ("sample.mp3", "audio/mpeg"),
    ("sample.wav", "audio/wav"),
    ("sample.m4a", "audio/mp4"),
    ("sample.flac", "audio/flac"),
    ("sample.aac", "audio/aac"),
    ("sample.ogg", "audio/ogg"),
    ("sample.mp4", "video/mp4"),
    ("sample.avi", "video/x-msvideo"),
    ("sample.mov", "video/quicktime"),
    ("sample.mkv", "video/x-matroska"),
])
def test_supported_media_formats(filename, content_type):
    validate_uploaded_file(_upload(filename, content_type))


def test_file_too_large(monkeypatch):
    from app.utils import validators as validators_module

    monkeypatch.setattr(validators_module, "MAX_FILE_SIZE", 0)

    with pytest.raises(HTTPException, match="maximum size"):
        validate_uploaded_file(_upload())


def test_empty_file():
    with pytest.raises(HTTPException, match="empty"):
        validate_uploaded_file(_upload(content=b""))


def test_filename_sanitization():
    assert sanitize_filename("../réunion finale?.wav") == "r_union_finale_.wav"


def test_uuid_generation():
    generated = generate_unique_filename("sample.wav")

    assert generated.endswith("_sample.wav")
    assert UUID(generated.split("_", 1)[0])


def test_file_saved(tmp_path, monkeypatch):
    monkeypatch.setattr(file_service_module, "UPLOAD_FOLDER", str(tmp_path))
    file = _upload(content=b"stored content")

    result = save_uploaded_file(file)

    assert Path(result["path"]).read_bytes() == b"stored content"


def test_upload_response():
    from app.schemas.upload_schema import UploadResponse

    response = UploadResponse(
        success=True,
        message="ok",
        file_id="file-id",
        original_filename="sample.wav",
        stored_filename="stored.wav",
        content_type="audio/wav",
    )

    assert response.success is True
    assert response.content_type == "audio/wav"


def test_upload_error_handling(tmp_path, monkeypatch):
    monkeypatch.setattr(file_service_module, "UPLOAD_FOLDER", str(tmp_path))
    file = _upload()

    def fail_copy(*args, **kwargs):
        raise OSError("disk unavailable")

    monkeypatch.setattr(file_service_module.shutil, "copyfileobj", fail_copy)

    with pytest.raises(OSError, match="disk unavailable"):
        save_uploaded_file(file)
