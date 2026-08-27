from uuid import UUID

from fastapi import APIRouter, BackgroundTasks
from fastapi import HTTPException
from fastapi import status

from app.schemas.process_schema import ProcessResponse
from app.services.process_service import ProcessService

router = APIRouter(
    prefix="/process",
    tags=["Process"]
)

process_service = ProcessService()


@router.post(
    "/start",
    response_model=ProcessResponse
)
async def start_process(
    file_id: UUID,
    background_tasks: BackgroundTasks,
    language: str = "auto",
) -> ProcessResponse:

    try:
        processing, pipeline = await process_service.prepare_process(
            file_id,
            language,
        )
        background_tasks.add_task(
            process_service.execute_background,
            file_id,
            processing,
            pipeline,
        )
        return ProcessResponse(
            success=True,
            message="Traitement démarré.",
            processing=processing,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
