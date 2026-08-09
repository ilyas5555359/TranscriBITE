from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus


class ProcessingStep(BaseModel):

    step: PipelineStep = Field(..., description="Nom de l'étape du pipeline")
    status: StepStatus = Field(..., description="Statut actuel de l'étape")
    message: Optional[str] = Field(
        default=None,
        description="Message d'information ou d'erreur"
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="Date et heure de début de l'étape"
    )
    finished_at: Optional[datetime] = Field(
        default=None,
        description="Date et heure de fin de l'étape"
    )


class ProcessingStatus(BaseModel):

    file_id: str = Field(..., description="Identifiant unique du fichier")

    current_step: PipelineStep = Field(
        ...,
        description="Étape actuellement exécutée"
    )

    current_status: StepStatus = Field(
        ...,
        description="Statut de l'étape actuelle"
    )

    progress_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Pourcentage d'avancement"
    )

    steps: list[ProcessingStep] = Field(
        default_factory=list,
        description="Liste complète des étapes du pipeline"
    )

    started_at: Optional[datetime] = Field(
        default=None,
        description="Date et heure de début du traitement"
    )

    finished_at: Optional[datetime] = Field(
        default=None,
        description="Date et heure de fin du traitement"
    )


class ProcessResponse(BaseModel):

    success: bool = Field(
        ...,
        description="Indique si le lancement du traitement a réussi"
    )

    message: str = Field(
        ...,
        description="Message destiné au frontend"
    )

    processing: ProcessingStatus = Field(
        ...,
        description="État actuel du traitement"
    )
