"""Schema standardisé pour les réponses d'erreur de l'API."""

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Réponse d'erreur standardisée."""

    success: bool = Field(
        default=False,
        description="Toujours False pour une erreur"
    )

    error: str = Field(
        ...,
        description="Type d'erreur"
    )

    detail: str = Field(
        ...,
        description="Description détaillée de l'erreur"
    )

    status_code: int = Field(
        ...,
        description="Code HTTP de l'erreur"
    )
