import asyncio
from pathlib import Path
from uuid import uuid4

import pytest

from app.enums.pipeline_step import PipelineStep
from app.enums.step_status import StepStatus
from app.schemas.process_schema import ProcessingStatus
from app.services import process_service as process_service_module
from app.services.process_service import ProcessService
from app.services.quality_service import quality_service
from app.services.summary_service import summary_service
from app.services.transcription_service import transcription_service


TRANSCRIPTION = {
    "text": "Texte de test",
    "language": "fr",
    "segments": [{"start": 0.0, "end": 1.0, "text": "Texte de test"}],
}


def _service(tmp_path, filename="sample.wav"):
    file_id = uuid4()
    (tmp_path / f"{file_id.hex}_{filename}").write_bytes(b"audio")
    service = ProcessService()
    return service, file_id


def _mock_pipeline_dependencies(monkeypatch):
    async def mock_quality(_):
        return {"duration": 1.0, "file_size": 5, "bitrate": 0,
                "sample_rate": 16000, "channels": 1}

    async def mock_summary(**_):
        return {"summary": "Résumé de test", "model": "test-model"}

    monkeypatch.setattr(quality_service, "analyze_audio", mock_quality)
    monkeypatch.setattr(summary_service, "generate_summary", mock_summary)


def test_start_process_success(tmp_path, monkeypatch):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(transcription_service, "transcribe", lambda _, **__: TRANSCRIPTION)
    _mock_pipeline_dependencies(monkeypatch)
    service, file_id = _service(tmp_path)

    response = asyncio.run(service.start_process(file_id))

    assert response.success is True
    assert response.processing.current_status == StepStatus.COMPLETED
    assert response.processing.transcription_result == TRANSCRIPTION


def test_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))

    with pytest.raises(FileNotFoundError, match="Fichier introuvable"):
        asyncio.run(ProcessService().start_process(uuid4()))


def test_invalid_uuid():
    from fastapi import FastAPI
    from app.routers.process import router

    app = FastAPI()
    app.include_router(router)

    assert any(route.path == "/process/start" for route in router.routes)


def test_audio_pipeline():
    pipeline = asyncio.run(ProcessService()._select_pipeline("audio"))

    assert PipelineStep.AUDIO_EXTRACTION not in pipeline
    assert pipeline[0] == PipelineStep.UPLOAD
    assert pipeline[-1] == PipelineStep.COMPLETED


def test_video_pipeline():
    pipeline = asyncio.run(ProcessService()._select_pipeline("video"))

    assert PipelineStep.AUDIO_EXTRACTION in pipeline
    assert pipeline.index(PipelineStep.AUDIO_EXTRACTION) < pipeline.index(PipelineStep.TRANSCRIPTION)


@pytest.mark.parametrize(
    "extension, expected_type",
    [
        (".mp3", "audio"),
        (".wav", "audio"),
        (".m4a", "audio"),
        (".flac", "audio"),
        (".aac", "audio"),
        (".ogg", "audio"),
        (".mp4", "video"),
        (".avi", "video"),
        (".mov", "video"),
        (".mkv", "video"),
    ],
)
def test_supported_formats_are_routed(tmp_path, monkeypatch, extension, expected_type):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    service, file_id = _service(tmp_path, f"sample{extension}")

    assert asyncio.run(service._detect_media_type(file_id)) == expected_type


def test_processing_status_creation():
    file_id = uuid4()
    processing = asyncio.run(ProcessService()._initialize_processing(file_id))

    assert processing.file_id == str(file_id)
    assert processing.current_step == PipelineStep.UPLOAD
    assert processing.current_status == StepStatus.PENDING
    assert processing.progress_percentage == 0.0
    assert all(step.step not in {PipelineStep.FAILED, PipelineStep.COMPLETED} for step in processing.steps)


def test_process_response(tmp_path, monkeypatch):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(transcription_service, "transcribe", lambda _, **__: TRANSCRIPTION)
    _mock_pipeline_dependencies(monkeypatch)
    service, file_id = _service(tmp_path)

    response = asyncio.run(service.start_process(file_id))

    assert response.model_dump()["success"] is True
    assert isinstance(response.processing, ProcessingStatus)


def test_pipeline_execution(tmp_path, monkeypatch):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(transcription_service, "transcribe", lambda _, **__: TRANSCRIPTION)
    _mock_pipeline_dependencies(monkeypatch)
    service, file_id = _service(tmp_path)
    processing = asyncio.run(service._initialize_processing(file_id))
    asyncio.run(service.progress_service.processing_state.add_processing(file_id, processing))

    asyncio.run(service._execute_pipeline(
        file_id,
        processing,
        asyncio.run(service._select_pipeline("audio")),
    ))

    assert processing.transcription_result == TRANSCRIPTION
    transcription_step = next(
        step for step in processing.steps
        if step.step == PipelineStep.TRANSCRIPTION
    )
    assert transcription_step.status == StepStatus.COMPLETED


def test_error_handling(tmp_path, monkeypatch):
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    _mock_pipeline_dependencies(monkeypatch)
    monkeypatch.setattr(
        transcription_service,
        "transcribe",
        lambda _, **__: (_ for _ in ()).throw(RuntimeError("transcription failed")),
    )
    service, file_id = _service(tmp_path)

    with pytest.raises(RuntimeError, match="transcription failed"):
        asyncio.run(service.start_process(file_id))

    processing = asyncio.run(service.progress_service.processing_state.get_processing(file_id))
    assert processing.current_step == PipelineStep.FAILED
    assert processing.current_status == StepStatus.FAILED
