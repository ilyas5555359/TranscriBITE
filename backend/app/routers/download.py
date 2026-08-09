from uuid import UUID

from fastapi import APIRouter

from app.schemas.download_schema import DownloadResponse
from app.services.download_service import DownloadService


router = APIRouter(
    prefix="/download",
    tags=["Download"]
)

download_service = DownloadService()


@router.get(
    "/{file_id}/{download_format}",
    response_model=DownloadResponse
)
async def prepare_download(
    file_id: UUID,
    download_format: str
) -> DownloadResponse:

    result = await download_service.prepare_download(
        file_id=file_id,
        download_format=download_format
    )

    return DownloadResponse(
        success=True,
        message="Téléchargement prêt.",
        file_id=result["file_id"],
        filename=result["filename"],
        download_format=result["download_format"]
    )
