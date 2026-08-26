from datetime import datetime
from pathlib import Path
from uuid import UUID

from app.config import UPLOAD_FOLDER
from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus
from app.schemas.process_schema import (
    ProcessResponse,
    ProcessingStatus,
    ProcessingStep,
)
from app.services.audio_service import audio_service
from app.services.progress_service import ProgressService
from app.services.transcription_service import (
    transcription_service,
)
from app.utils.logger import logger


class ProcessService:

    def __init__(self):
        self.progress_service = ProgressService()

    async def start_process(
        self,
        file_id: UUID
    ) -> ProcessResponse:

        try:
            processing = await self._initialize_processing(file_id)

            await self.progress_service.processing_state.add_processing(
                file_id,
                processing
            )

            await self._log_process_started(file_id)

            await self._validate_file(file_id)

            media_type = await self._detect_media_type(file_id)

            pipeline = await self._select_pipeline(media_type)

            await self._execute_pipeline(
                file_id=file_id,
                processing=processing,
                pipeline=pipeline
            )

            await self._finalize_processing(
                file_id,
                processing
            )

            await self._log_process_completed(file_id)

            return ProcessResponse(
                success=True,
                message="Traitement terminé avec succès.",
                processing=processing
            )

        except Exception as error:
            await self._handle_error(
                file_id,
                error
            )
            raise

    async def _validate_file(
        self,
        file_id: UUID
    ) -> Path:

        upload_folder = Path(UPLOAD_FOLDER)

        if not upload_folder.is_dir():
            raise FileNotFoundError(
                "Le dossier des fichiers uploadés est introuvable."
            )

        file_prefix = f"{file_id.hex}_"

        matches = [
            path
            for path in upload_folder.iterdir()
            if path.is_file()
            and path.name.startswith(file_prefix)
        ]

        if not matches:
            raise FileNotFoundError(
                f"Fichier introuvable pour le file_id: {file_id}"
            )

        if len(matches) > 1:
            raise ValueError(
                f"Plusieurs fichiers correspondent au file_id: {file_id}"
            )

        return matches[0]

    async def _initialize_processing(
        self,
        file_id: UUID
    ) -> ProcessingStatus:

        steps = [
            ProcessingStep(
                step=step,
                status=StepStatus.PENDING
            )
            for step in PipelineStep
            if step not in {
                PipelineStep.FAILED,
                PipelineStep.COMPLETED,
            }
        ]

        return ProcessingStatus(
            file_id=str(file_id),
            current_step=PipelineStep.UPLOAD,
            current_status=StepStatus.PENDING,
            progress_percentage=0.0,
            steps=steps,
            started_at=datetime.now(),
            finished_at=None
        )

    async def _detect_media_type(
        self,
        file_id: UUID
    ) -> str:

        file_path = await self._validate_file(file_id)

        extension = file_path.suffix.lower()

        audio_extensions = {
            ".mp3",
            ".wav",
            ".m4a",
            ".flac",
            ".aac",
            ".ogg",
        }

        video_extensions = {
            ".mp4",
            ".avi",
            ".mov",
            ".mkv",
        }

        if extension in audio_extensions:
            return "audio"

        if extension in video_extensions:
            return "video"

        raise ValueError(
            f"Format média non supporté: {extension}"
        )

    async def _select_pipeline(
        self,
        media_type: str
    ) -> list[PipelineStep]:

        if media_type == "audio":
            return [
                PipelineStep.UPLOAD,
                PipelineStep.VALIDATION,
                PipelineStep.TRANSCRIPTION,
                PipelineStep.RESULT_PREPARATION,
                PipelineStep.COMPLETED,
            ]

        if media_type == "video":
            return [
                PipelineStep.UPLOAD,
                PipelineStep.VALIDATION,
                PipelineStep.AUDIO_EXTRACTION,
                PipelineStep.TRANSCRIPTION,
                PipelineStep.RESULT_PREPARATION,
                PipelineStep.COMPLETED,
            ]

        raise ValueError(
            "Type de média non supporté."
        )

    async def _execute_pipeline(
        self,
        file_id: UUID,
        processing: ProcessingStatus,
        pipeline: list[PipelineStep]
    ) -> None:

        total_steps = len(pipeline)

        for index, step in enumerate(pipeline):

            if step == PipelineStep.COMPLETED:
                continue

            await self.progress_service.update_current_step(
                file_id,
                step
            )

            await self.progress_service.update_step_status(
                file_id,
                step,
                StepStatus.IN_PROGRESS
            )

            await self._log_step_started(step)

            try:

                if step == PipelineStep.UPLOAD:
                    pass

                elif step == PipelineStep.VALIDATION:
                    await self._validate_file(file_id)

                elif step == PipelineStep.AUDIO_EXTRACTION:
                    await self._extract_audio(file_id)

                elif step == PipelineStep.TRANSCRIPTION:
                    await self._transcribe_audio(file_id)

                elif step == PipelineStep.RESULT_PREPARATION:
                    await self._prepare_results(file_id)

                await self.progress_service.update_step_status(
                    file_id,
                    step,
                    StepStatus.COMPLETED
                )

                await self.progress_service.update_progress_percentage(
                    file_id
                )

                await self._log_step_completed(step)

            except Exception as error:

                await self.progress_service.fail_processing(
                    file_id,
                    str(error)
                )

                raise

    async def _extract_audio(
        self,
        file_id: UUID
    ) -> str:

        source_path = await self._validate_file(file_id)

        result = await audio_service.extract_audio(
            source_path
        )

        return result["audio_path"]

    async def _transcribe_audio(
        self,
        file_id: UUID
    ) -> dict:

        source_path = await self._validate_file(file_id)

        media_type = await self._detect_media_type(
            file_id
        )

        if media_type == "video":
            extracted = await audio_service.extract_audio(
                source_path
            )
            audio_path = extracted["audio_path"]

        else:
            audio_path = str(source_path)

        result = transcription_service.transcribe(
            audio_path
        )

        logger.info(
            "Transcription completed for %s",
            file_id
        )

        return result

    async def _prepare_results(
        self,
        file_id: UUID
    ) -> None:

        logger.info(
            "Préparation des résultats pour %s",
            file_id
        )

    async def _finalize_processing(
        self,
        file_id: UUID,
        processing: ProcessingStatus
    ) -> None:

        await self.progress_service.complete_processing(
            file_id
        )

        processing.finished_at = datetime.now()

    async def _handle_error(
        self,
        file_id: UUID,
        error: Exception
    ) -> None:

        logger.error(
            "Erreur du traitement %s: %s",
            file_id,
            error
        )

        try:
            await self.progress_service.fail_processing(
                file_id,
                str(error)
            )
        except FileNotFoundError:
            pass

    async def _log_process_started(
        self,
        file_id: UUID
    ) -> None:

        logger.info(
            "Traitement démarré: %s",
            file_id
        )

    async def _log_step_started(
        self,
        step: PipelineStep
    ) -> None:

        logger.info(
            "Étape démarrée: %s",
            step.value
        )

    async def _log_step_completed(
        self,
        step: PipelineStep
    ) -> None:

        logger.info(
            "Étape terminée: %s",
            step.value
        )

    async def _log_process_completed(
        self,
        file_id: UUID
    ) -> None:

        logger.info(
            "Traitement terminé: %s",
            file_id
        )