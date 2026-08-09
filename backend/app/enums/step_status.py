from enum import Enum


class StepStatus(str, Enum):
    PENDING = "En attente"
    IN_PROGRESS = "En cours"
    COMPLETED = "Terminée"
    FAILED = "Échec"
