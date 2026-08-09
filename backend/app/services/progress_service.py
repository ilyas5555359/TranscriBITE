from uuid import UUID
from datetime import datetime

from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus

from app.models.processing_state import ProcessingState

from app.schemas.process_schema import ProcessingStatus

from app.schemas.progress_schema import ProgressResponse


class ProgressService:

    def __init__(self):

        self.processing_state = ProcessingState()

    async def get_progress(
        self,
        file_id: UUID
    ) -> ProgressResponse:

        processing = await self.get_processing_status(
            file_id
        )

        return ProgressResponse(
            success=True,
            message="Progression récupérée avec succès.",
            processing=processing
        )

    async def get_processing_status(
        self,
        file_id: UUID
    ) -> ProcessingStatus:

        processing = await self.processing_state.get_processing(
            file_id
        )

        if processing is None:

            raise FileNotFoundError(
                "Traitement introuvable."
            )

        return processing


    async def update_current_step(
        self,
        file_id: UUID,
        step: PipelineStep
    ) -> None:

        processing = await self.get_processing_status(
            file_id
        )

        processing.current_step = step


    async def update_step_status(
        self,
        file_id: UUID,
        step: PipelineStep,
        status: StepStatus
    ) -> None:

        processing = await self.get_processing_status(
            file_id
        )

        for processing_step in processing.steps:

            if processing_step.step == step:

                processing_step.status = status

                break

        processing.current_status = status


    async def update_progress_percentage(
        self,
        file_id: UUID
    ) -> None:

        processing = await self.get_processing_status(
            file_id
        )

        completed_steps = sum(
            1
            for step in processing.steps
            if step.status == StepStatus.COMPLETED
        )

        total_steps = len(processing.steps)

        if total_steps == 0:

            processing.progress_percentage = 0.0

            return

        processing.progress_percentage = round(
            (completed_steps / total_steps) * 100,
            2
        )


    async def complete_processing(
        self,
        file_id: UUID
    ) -> None:

        processing = await self.get_processing_status(
            file_id
        )

        processing.current_step = PipelineStep.COMPLETED

        processing.current_status = StepStatus.COMPLETED

        processing.progress_percentage = 100.0

        processing.finished_at = datetime.now()


    async def fail_processing(
        self,
        file_id: UUID,
        message: str
    ) -> None:

        processing = await self.get_processing_status(
            file_id
        )

        processing.current_step = PipelineStep.FAILED

        processing.current_status = StepStatus.FAILED

        processing.finished_at = datetime.now()

        for step in processing.steps:

            if step.step == processing.current_step:

                step.status = StepStatus.FAILED

                step.message = message

                break


    async def _log_progress_started(
        self,
        file_id: UUID
    ) -> None:

        raise NotImplementedError(
            "Logger en cours de développement."
        )


    async def _log_step_updated(
        self,
        step: PipelineStep
    ) -> None:

        raise NotImplementedError(
            "Logger en cours de développement."
        )


    async def _log_progress_updated(
        self,
        progress: float
    ) -> None:

        raise NotImplementedError(
            "Logger en cours de développement."
        )


    async def _log_progress_completed(
        self,
        file_id: UUID
    ) -> None:

        raise NotImplementedError(
            "Logger en cours de développement."
        )


    async def _log_error(
        self,
        error: Exception
    ) -> None:

        raise NotImplementedError(
            "Logger en cours de développement."
        )
