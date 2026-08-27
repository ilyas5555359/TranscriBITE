"""Routes REST pour la transcription audio."""

from pathlib import Path
from uuid import UUID

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
from app.config import OUTPUT_FOLDER, UPLOAD_FOLDER
from app.models.processing_state import processing_state

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
        job_id = UUID(request.job_id)
        if not await processing_state.exists(job_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Traitement introuvable.",
            )

        audio_path = Path(request.audio_path).resolve()
        allowed_roots = (
            Path(UPLOAD_FOLDER).resolve(),
            Path(OUTPUT_FOLDER).resolve(),
        )
        if not any(
            audio_path.is_relative_to(root)
            and audio_path.name.startswith(f"{job_id.hex}_")
            for root in allowed_roots
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chemin audio non autorisé.",
            )

        result = transcription_service.transcribe(
            str(audio_path)
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
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_id invalide.",
        ) from error