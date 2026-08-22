"""Schemas de l'API de transcription."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class TranscribeRequest(BaseModel):
    """Données nécessaires pour lancer une transcription."""

    job_id: str = Field(
        ...,
        min_length=1,
        description="Identifiant partagé du traitement"
    )

    audio_path: str = Field(
        ...,
        min_length=1,
        description="Chemin du fichier audio prêt à transcrire"
    )

    original_filename: str = Field(
        ...,
        min_length=1,
        description="Nom original du fichier"
    )

    media_type: Literal["audio"] = Field(
        ...,
        description="Type de média attendu par l'endpoint"
    )


class TranscriptionData(BaseModel):
    """Résultat d'une transcription Faster-Whisper."""

    text: str = Field(
        ...,
        description="Texte transcrit"
    )

    language: str = Field(
        ...,
        description="Langue détectée"
    )

    segments: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Segments avec timestamps"
    )


class TranscribeResponse(BaseModel):
    """Réponse de l'API de transcription."""

    success: bool = Field(
        ...,
        description="Indique si la transcription a réussi"
    )

    message: str = Field(
        ...,
        description="Message destiné au frontend"
    )

    data: TranscriptionData | None = Field(
        default=None,
        description="Résultat de la transcription"
    )

    job_id: str = Field(
        ...,
        description="Identifiant partagé du traitement"
    )