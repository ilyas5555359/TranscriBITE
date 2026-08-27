"""Route d'upload de fichiers audio/vidéo."""

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.schemas.upload_schema import UploadResponse
from app.services.file_service import save_uploaded_file
from app.utils.validators import validate_uploaded_file
from app.utils.logger import logger


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post(
    "/",
    response_model=UploadResponse,
)
async def upload_file(file: UploadFile = File(...)):
    """Uploader un fichier audio ou vidéo."""

    logger.info(f"Upload request received: {file.filename}")

    try:
        validate_uploaded_file(file)

        result = save_uploaded_file(file)

        return UploadResponse(
            success=True,
            message="Fichier uploadé avec succès.",
            file_id=result["file_id"],
            original_filename=file.filename,
            stored_filename=result["stored_filename"],
            content_type=file.content_type,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
