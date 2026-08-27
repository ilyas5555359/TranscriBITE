"""Routes REST pour la génération de résumé via Ollama."""

from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from app.schemas.summary_schema import (
    SummaryRequest,
    SummaryResponse,
    SummaryData,
)
from app.services.summary_service import (
    SummaryError,
    summary_service,
)
from app.models.processing_state import processing_state

router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)


@router.post(
    "",
    response_model=SummaryResponse,
)
async def generate_summary(
    request: SummaryRequest,
) -> SummaryResponse:
    """Générer un résumé du texte transcrit."""

    try:
        job_id = UUID(request.job_id)
        if not await processing_state.exists(job_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Traitement introuvable.",
            )

        result = await summary_service.generate_summary(
            text=request.text,
            language=request.language,
        )

        return SummaryResponse(
            success=True,
            message="Résumé généré avec succès",
            data=SummaryData(**result),
            job_id=request.job_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except SummaryError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
