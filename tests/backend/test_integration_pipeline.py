import asyncio

from fastapi.testclient import TestClient

from app.main import app
from app.models.processing_state import processing_state
from app.routers import download as download_router
from app.routers import upload as upload_router
from app.services import file_service as file_service_module
from app.services import process_service as process_service_module
from app.services.quality_service import quality_service
from app.services.summary_service import summary_service
from app.services.transcription_service import transcription_service


def test_http_pipeline_upload_process_progress_download(tmp_path, monkeypatch):
    monkeypatch.setattr(file_service_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(process_service_module, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(download_router.download_service, "_output_folder", tmp_path)
    monkeypatch.setattr(
        quality_service,
        "analyze_audio",
        lambda _path: asyncio.sleep(0, result={
            "duration": 1.0,
            "file_size": 5,
            "bitrate": 0,
            "sample_rate": 16000,
            "channels": 1,
        }),
    )
    monkeypatch.setattr(
        transcription_service,
        "transcribe",
        lambda _path, **_: {
            "text": "Bonjour integration",
            "language": "fr",
            "segments": [],
        },
    )
    monkeypatch.setattr(
        summary_service,
        "generate_summary",
        lambda **_: asyncio.sleep(0, result={
            "summary": "Résumé integration",
            "model": "test-model",
        }),
    )

    client = TestClient(app)
    upload = client.post(
        "/upload/",
        files={"file": ("sample.wav", b"audio", "audio/wav")},
    )
    assert upload.status_code == 200
    file_id = upload.json()["file_id"]

    started = client.post(f"/process/start?file_id={file_id}&language=fr")
    assert started.status_code == 200
    assert started.json()["processing"]["current_status"] in {
        "En attente",
        "Terminée",
    }

    progress = client.get(f"/progress/{file_id}")
    assert progress.status_code == 200
    assert progress.json()["processing"]["current_status"] == "Terminée"
    assert progress.json()["processing"]["summary_result"]["summary"] == (
        "Résumé integration"
    )

    txt = client.get(f"/download/{file_id}/txt")
    assert txt.status_code == 200
    assert "Résumé integration" in txt.text

    result = client.get(f"/download/{file_id}/json")
    assert result.status_code == 200
    assert result.json()["summary"]["model"] == "test-model"

    asyncio.run(processing_state.remove_processing(file_id))
