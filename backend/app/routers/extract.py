"""HTTP endpoint for extracting a Faster-Whisper compatible WAV file."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from app.config import UPLOAD_FOLDER
from app.schemas.extract_schema import (
    ExtractErrorResponse,
    ExtractRequest,
    ExtractResponse,
)
from app.services.audio_service import (
    AudioExtractionException,
    FFmpegException,
    audio_service,
)
from app.utils.logger import logger


router = APIRouter(prefix="/extract", tags=["Extract"])


def _find_uploaded_file(file_id: str) -> Path:
    """Resolve an upload ID without accepting path traversal input."""
    if Path(file_id).name != file_id:
        raise FileNotFoundError("Uploaded file not found")

    upload_folder = Path(UPLOAD_FOLDER)
    if not upload_folder.is_dir():
        raise FileNotFoundError("Uploaded file not found")

    matches = [
        path
        for path in upload_folder.iterdir()
        if path.is_file()
        and (path.name == file_id or path.stem == file_id or path.name.startswith(f"{file_id}_"))
    ]
    if len(matches) != 1:
        raise FileNotFoundError("Uploaded file not found")
    return matches[0]


@router.post(
    "",
    response_model=ExtractResponse,
    responses={
        404: {"model": ExtractErrorResponse},
        500: {"model": ExtractErrorResponse},
    },
)
async def extract_audio(request: ExtractRequest) -> ExtractResponse:
    """Create a mono, 16 kHz, PCM 16-bit WAV from an uploaded source."""
    try:
        source_path = _find_uploaded_file(request.file_id)
        result = await audio_service.extract_audio(source_path)
        return ExtractResponse(
            success=True,
            message="Audio extracted successfully",
            file_id=request.file_id,
            **result,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uploaded file not found",
        ) from exc
    except FFmpegException as exc:
        logger.error("FFmpeg is unavailable: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Audio extraction service is unavailable",
        ) from exc
    except AudioExtractionException as exc:
        logger.warning("Audio extraction failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Audio extraction failed",
        ) from exc
