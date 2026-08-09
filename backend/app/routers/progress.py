from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.schemas.progress_schema import ProgressResponse

from app.services.progress_service import ProgressService

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)

progress_service = ProgressService()

@router.get(
    "/{file_id}",
    response_model=ProgressResponse
)
async def get_progress(
    file_id: UUID
) -> ProgressResponse:

    try:

        return await progress_service.get_progress(
            file_id
        )

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
