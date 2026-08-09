from pydantic import BaseModel
from uuid import UUID


class DownloadResponse(BaseModel):

    success: bool

    message: str

    file_id: UUID

    filename: str

    download_format: str
