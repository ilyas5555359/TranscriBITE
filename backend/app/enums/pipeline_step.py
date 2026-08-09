from enum import Enum


class PipelineStep(str, Enum):
    UPLOAD = "Upload"
    VALIDATION = "Validation"
    MEDIA_DETECTION = "Détection du média"
    AUDIO_QUALITY_ANALYSIS = "Analyse qualité audio"
    AUDIO_EXTRACTION = "Extraction audio"
    TRANSCRIPTION = "Transcription"
    SUMMARY_GENERATION = "Génération résumé"
    RESULT_PREPARATION = "Préparation des résultats"
    CLEANUP = "Nettoyage"
    COMPLETED = "Terminé"
    FAILED = "Échoué"
