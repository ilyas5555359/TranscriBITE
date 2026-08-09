from uuid import UUID

from fastapi import APIRouter
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
    file_id: UUID
) -> ProcessResponse:

    try:
        return await process_service.start_process(file_id)

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
