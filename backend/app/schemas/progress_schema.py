from pydantic import BaseModel

from app.schemas.process_schema import ProcessingStatus


class ProgressResponse(BaseModel):

    success: bool

    message: str

    processing: ProcessingStatus
