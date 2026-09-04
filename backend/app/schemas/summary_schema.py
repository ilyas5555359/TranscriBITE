"""Schemas de l'API de résumé."""

from typing import Literal

from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    """Données nécessaires pour générer un résumé."""

    job_id: str = Field(
        ...,
        min_length=1,
        description="Identifiant partagé du traitement"
    )

    text: str = Field(
        ...,
        min_length=1,
        description="Texte transcrit à résumer"
    )

    language: str = Field(
        default="fr",
        description="Langue du texte"
    )

    summary_length: Literal["short", "normal", "long"] = Field(
        default="normal",
        description="Longueur souhaitée du résumé",
    )


class SummaryData(BaseModel):
    """Résultat d'un résumé généré par Ollama."""

    summary: str = Field(
        ...,
        description="Résumé du texte transcrit"
    )

    model: str = Field(
        ...,
        description="Modèle utilisé pour le résumé"
    )


class SummaryResponse(BaseModel):
    """Réponse de l'API de résumé."""

    success: bool = Field(
        ...,
        description="Indique si la génération du résumé a réussi"
    )

    message: str = Field(
        ...,
        description="Message destiné au frontend"
    )

    data: SummaryData | None = Field(
        default=None,
        description="Résultat du résumé"
    )

    job_id: str = Field(
        ...,
        description="Identifiant partagé du traitement"
    )
