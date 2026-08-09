from fastapi import APIRouter, UploadFile, File

from app.services.file_service import save_uploaded_file
from app.utils.validators import validate_uploaded_file
from app.utils.logger import logger

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    logger.info(f"Upload request received: {file.filename}")

    validate_uploaded_file(file)

    saved_file = save_uploaded_file(file)

    return {
    "original_filename": file.filename,
    "stored_filename": saved_file.name,
    "content_type": file.content_type,
    "saved_to": str(saved_file)
    }
