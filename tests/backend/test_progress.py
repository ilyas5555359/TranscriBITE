import asyncio
from uuid import uuid4

import pytest

from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus
from app.schemas.process_schema import ProcessingStatus, ProcessingStep
from app.services.progress_service import ProgressService


def _processing(file_id, statuses=None):
    statuses = statuses or {
        PipelineStep.UPLOAD: StepStatus.PENDING,
        PipelineStep.VALIDATION: StepStatus.PENDING,
        PipelineStep.TRANSCRIPTION: StepStatus.PENDING,
    }
    return ProcessingStatus(
        file_id=str(file_id),
        current_step=PipelineStep.UPLOAD,
        current_status=StepStatus.PENDING,
        steps=[
            ProcessingStep(step=step, status=status)
            for step, status in statuses.items()
        ],
    )


def _service_with_processing(processing, file_id):
    service = ProgressService()
    asyncio.run(service.processing_state.add_processing(file_id, processing))
    return service


def test_get_progress_success():
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    response = asyncio.run(service.get_progress(file_id))

    assert response.success is True
    assert response.processing.file_id == str(file_id)


def test_processing_not_found():
    with pytest.raises(FileNotFoundError, match="Traitement introuvable"):
        asyncio.run(ProgressService().get_processing_status(uuid4()))


def test_update_current_step():
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    asyncio.run(service.update_current_step(file_id, PipelineStep.TRANSCRIPTION))

    processing = asyncio.run(service.get_processing_status(file_id))
    assert processing.current_step == PipelineStep.TRANSCRIPTION


def test_update_step_status():
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    asyncio.run(service.update_step_status(
        file_id,
        PipelineStep.TRANSCRIPTION,
        StepStatus.IN_PROGRESS,
    ))

    processing = asyncio.run(service.get_processing_status(file_id))
    assert processing.current_status == StepStatus.IN_PROGRESS
    assert processing.steps[-1].status == StepStatus.IN_PROGRESS


def test_progress_percentage():
    file_id = uuid4()
    service = _service_with_processing(
        _processing(file_id, {
            PipelineStep.UPLOAD: StepStatus.COMPLETED,
            PipelineStep.VALIDATION: StepStatus.COMPLETED,
            PipelineStep.TRANSCRIPTION: StepStatus.PENDING,
        }),
        file_id,
    )

    asyncio.run(service.update_progress_percentage(file_id))

    processing = asyncio.run(service.get_processing_status(file_id))
    assert processing.progress_percentage == pytest.approx(66.67)


def test_complete_processing():
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    asyncio.run(service.complete_processing(file_id))

    processing = asyncio.run(service.get_processing_status(file_id))
    assert processing.current_step == PipelineStep.COMPLETED
    assert processing.current_status == StepStatus.COMPLETED
    assert processing.progress_percentage == 100.0
    assert processing.finished_at is not None


def test_fail_processing_marks_active_step():
    file_id = uuid4()
    service = _service_with_processing(_processing(
        file_id,
        {
            PipelineStep.UPLOAD: StepStatus.COMPLETED,
            PipelineStep.TRANSCRIPTION: StepStatus.IN_PROGRESS,
        },
    ), file_id)

    asyncio.run(service.fail_processing(file_id, "transcription failed"))

    processing = asyncio.run(service.get_processing_status(file_id))
    assert processing.current_step == PipelineStep.FAILED
    assert processing.current_status == StepStatus.FAILED
    assert processing.steps[-1].status == StepStatus.FAILED
    assert processing.steps[-1].message == "transcription failed"


def test_progress_response():
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    response = asyncio.run(service.get_progress(file_id))

    assert response.model_dump()["success"] is True
    assert response.model_dump()["processing"]["file_id"] == str(file_id)


def test_logger(caplog):
    file_id = uuid4()
    service = _service_with_processing(_processing(file_id), file_id)

    with caplog.at_level("INFO"):
        asyncio.run(service.complete_processing(file_id))

    assert str(file_id) in caplog.text
