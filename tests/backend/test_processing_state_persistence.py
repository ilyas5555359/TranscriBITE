import asyncio
from uuid import uuid4

from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus
from app.models.processing_state import ProcessingState
from app.schemas.process_schema import ProcessingStatus
from app.services.progress_service import ProgressService


def test_processing_state_survives_new_instance(tmp_path):
    state_file = tmp_path / "processing_states.json"
    file_id = uuid4()
    processing = ProcessingStatus(
        file_id=str(file_id),
        current_step=PipelineStep.TRANSCRIPTION,
        current_status=StepStatus.IN_PROGRESS,
    )

    first_state = ProcessingState(state_file)
    asyncio.run(first_state.add_processing(file_id, processing))

    second_state = ProcessingState(state_file)
    restored = asyncio.run(second_state.get_processing(file_id))

    assert restored is not None
    assert restored.file_id == str(file_id)
    assert restored.current_step == PipelineStep.TRANSCRIPTION


def test_processing_state_persists_progress_updates(tmp_path):
    state = ProcessingState(tmp_path / "processing_states.json")
    service = ProgressService()
    service.processing_state = state
    file_id = uuid4()
    processing = ProcessingStatus(
        file_id=str(file_id),
        current_step=PipelineStep.UPLOAD,
        current_status=StepStatus.PENDING,
        steps=[{"step": PipelineStep.UPLOAD, "status": StepStatus.PENDING}],
    )

    asyncio.run(state.add_processing(file_id, processing))
    asyncio.run(service.update_current_step(file_id, PipelineStep.UPLOAD))
    asyncio.run(service.update_step_status(
        file_id,
        PipelineStep.UPLOAD,
        StepStatus.COMPLETED,
    ))
    asyncio.run(service.update_progress_percentage(file_id))

    restored = ProcessingState(tmp_path / "processing_states.json")
    saved = asyncio.run(restored.get_processing(file_id))
    assert saved is not None
    assert saved.progress_percentage == 100.0