"""Schemas pour l'endpoint upload."""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Réponse de l'API après un upload réussi."""

    success: bool = Field(
        ...,
        description="Indique si l'upload a réussi"
    )

    message: str = Field(
        ...,
        description="Message destiné au frontend"
    )

    file_id: str = Field(
        ...,
        description="Identifiant UUID unique du fichier uploadé"
    )

    original_filename: str = Field(
        ...,
        description="Nom original du fichier"
    )

    stored_filename: str = Field(
        ...,
        description="Nom du fichier tel que stocké sur le serveur"
    )

    content_type: str | None = Field(
        default=None,
        description="Type MIME du fichier"
    )
