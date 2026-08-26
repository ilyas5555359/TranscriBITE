"""Pydantic contracts for audio extraction."""

from typing import Literal

from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    """Identify an uploaded source file and request a Whisper-ready WAV."""

    file_id: str = Field(..., min_length=1, description="Uploaded file identifier")
    output_format: Literal["wav"] = Field(
        default="wav",
        description="Output format; WAV is required by the extraction pipeline",
    )


class ExtractResponse(BaseModel):
    """Successful extraction result."""

    success: bool = True
    message: str
    file_id: str
    audio_filename: str
    audio_path: str


class ExtractErrorResponse(BaseModel):
    """Public error shape documented for the endpoint."""

    success: bool = False
    message: str
