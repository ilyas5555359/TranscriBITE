"""Route de téléchargement des résultats de transcription."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from pathlib import Path

from app.services.download_service import DownloadService


router = APIRouter(
    prefix="/download",
    tags=["Download"]
)

download_service = DownloadService()


MEDIA_TYPES = {
    "txt": "text/plain",
    "json": "application/json",
    "pdf": "application/pdf",
}


@router.get(
    "/{file_id}/{download_format}",
)
async def download_file(
    file_id: UUID,
    download_format: str,
):
    """Télécharger le résultat de transcription (TXT ou JSON)."""

    try:
        result = await download_service.prepare_download(
            file_id=file_id,
            download_format=download_format,
        )

        file_path = Path(result["file_path"])

        if not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Le fichier généré est introuvable.",
            )

        return FileResponse(
            path=str(file_path),
            filename=result["filename"],
            media_type=MEDIA_TYPES.get(download_format, "application/octet-stream"),
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
