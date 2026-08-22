"""Routes REST pour la transcription audio."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.transcription_schema import (
    TranscribeRequest,
    TranscribeResponse,
    TranscriptionData,
)
from app.services.transcription_service import (
    TranscriptionError,
    transcription_service,
)

router = APIRouter(
    prefix="/transcribe",
    tags=["Transcription"],
)


@router.post(
    "",
    response_model=TranscribeResponse,
)
async def transcribe(
    request: TranscribeRequest,
) -> TranscribeResponse:
    """Transcrire un fichier audio déjà préparé."""

    try:
        result = transcription_service.transcribe(
            request.audio_path
        )

        return TranscribeResponse(
            success=True,
            message="Transcription completed successfully",
            data=TranscriptionData(**result),
            job_id=request.job_id,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found",
        ) from error

    except TranscriptionError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from error