import asyncio
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.models.processing_state import processing_state
from app.routers import summary as summary_router
from app.routers import transcription as transcription_router
from app.schemas.summary_schema import SummaryRequest
from app.schemas.transcription_schema import TranscribeRequest
from app.routers import transcription as transcription_router_module
from app.routers import summary as summary_router_module


def test_transcription_rejects_unknown_job(monkeypatch):
    request = TranscribeRequest(
        job_id=str(uuid4()),
        audio_path="ignored.wav",
        original_filename="sample.wav",
        media_type="audio",
    )

    with pytest.raises(HTTPException) as error:
        asyncio.run(transcription_router.transcribe(request))

    assert error.value.status_code == 404


def test_transcription_rejects_path_outside_storage(tmp_path, monkeypatch):
    job_id = uuid4()
    asyncio.run(processing_state.add_processing(job_id, object()))
    request = TranscribeRequest(
        job_id=str(job_id),
        audio_path=str(tmp_path / f"{job_id.hex}_sample.wav"),
        original_filename="sample.wav",
        media_type="audio",
    )

    with pytest.raises(HTTPException) as error:
        asyncio.run(transcription_router.transcribe(request))

    assert error.value.status_code == 400
    asyncio.run(processing_state.remove_processing(job_id))


def test_summary_rejects_unknown_job():
    request = SummaryRequest(job_id=str(uuid4()), text="Texte")

    with pytest.raises(HTTPException) as error:
        asyncio.run(summary_router.generate_summary(request))

    assert error.value.status_code == 404


def test_transcription_route_success(tmp_path, monkeypatch):
    job_id = uuid4()
    audio_path = tmp_path / f"{job_id.hex}_sample.wav"
    audio_path.write_bytes(b"audio")
    asyncio.run(processing_state.add_processing(job_id, object()))
    monkeypatch.setattr(transcription_router_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(
        transcription_router_module.transcription_service,
        "transcribe",
        lambda _path, **_: {
            "text": "Bonjour",
            "language": "fr",
            "segments": [],
        },
    )

    response = TestClient(app).post(
        "/transcribe",
        json={
            "job_id": str(job_id),
            "audio_path": str(audio_path),
            "original_filename": "sample.wav",
            "media_type": "audio",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["language"] == "fr"
    asyncio.run(processing_state.remove_processing(job_id))


def test_summary_route_success(monkeypatch):
    job_id = uuid4()
    asyncio.run(processing_state.add_processing(job_id, object()))

    async def fake_summary(**_):
        return {"summary": "Résumé", "model": "test-model"}

    monkeypatch.setattr(
        summary_router_module.summary_service,
        "generate_summary",
        fake_summary,
    )
    response = TestClient(app).post(
        "/summary",
        json={"job_id": str(job_id), "text": "Texte", "language": "fr"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["summary"] == "Résumé"
    asyncio.run(processing_state.remove_processing(job_id))