from app.enums.pipeline_step import PipelineStep

PIPELINE_ORDER = [
    PipelineStep.UPLOAD,
    PipelineStep.VALIDATION,
    PipelineStep.MEDIA_DETECTION,
    PipelineStep.AUDIO_QUALITY_ANALYSIS,
    PipelineStep.AUDIO_EXTRACTION,
    PipelineStep.TRANSCRIPTION,
    PipelineStep.SUMMARY_GENERATION,
    PipelineStep.RESULT_PREPARATION,
    PipelineStep.CLEANUP,
    PipelineStep.COMPLETED,
    PipelineStep.FAILED,
]
