import asyncio
import json
from datetime import datetime
from uuid import uuid4

import pytest

from app.models.processing_state import processing_state
from app.schemas.process_schema import ProcessingStatus
from app.services import download_service as download_service_module
from app.services.download_service import DownloadService


def _service_with_result(tmp_path, monkeypatch):
    monkeypatch.setattr(download_service_module, "OUTPUT_FOLDER", str(tmp_path))
    file_id = uuid4()
    processing = ProcessingStatus(
        file_id=str(file_id),
        original_filename="test_audio.mp3",
        current_step="Terminé",
        current_status="Terminée",
        started_at=datetime(2026, 8, 27, 14, 30, 0),
        finished_at=datetime(2026, 8, 27, 14, 31, 23),
        transcription_result={
            "text": "Texte de test",
            "language": "fr",
            "segments": [],
        },
        quality_result={
            "duration": 83.4,
            "file_size": 343130,
            "bitrate": 128000,
            "sample_rate": 44100,
            "channels": 2,
        },
        summary_result={
            "summary": "Résumé de test",
            "model": "test-model",
        },
    )
    asyncio.run(processing_state.add_processing(file_id, processing))
    return DownloadService(), file_id


def test_prepare_download_success(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "txt"))

    assert result["file_id"] == file_id
    assert result["download_format"] == "txt"
    assert result["file_path"]


def test_invalid_download_format(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    with pytest.raises(ValueError, match="non supporté"):
        asyncio.run(service.prepare_download(file_id, "csv"))


def test_txt_download(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "txt"))

    content = open(result["file_path"], encoding="utf-8").read()
    assert "Texte de test" in content
    assert "Résumé de test" in content


def test_json_download(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "json"))
    content = json.loads(open(result["file_path"], encoding="utf-8").read())

    assert content["file_id"] == str(file_id)
    assert content["transcription"]["language"] == "fr"
    assert content["summary"]["model"] == "test-model"


def test_pdf_download(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "pdf"))

    assert result["filename"].endswith(".pdf")
    assert open(result["file_path"], "rb").read(4) == b"%PDF"


def test_pdf_report_contains_processing_sections(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "pdf"))
    content = open(result["file_path"], "rb").read()

    assert b"RAPPORT DE TRANSCRIPTION" in content
    assert b"test_audio.mp3" in content
    assert b"Informations techniques" in content
    assert b"Aucun service cloud" in content
    assert b"Type : Audio" in content
    assert b"1 min 23 s" in content
    assert b"base" in content


def test_validate_download(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    asyncio.run(service._validate_download(file_id, "txt"))

    with pytest.raises(ValueError):
        asyncio.run(service._validate_download(file_id, "csv"))


def test_download_response(tmp_path, monkeypatch):
    service, file_id = _service_with_result(tmp_path, monkeypatch)

    result = asyncio.run(service.prepare_download(file_id, "txt"))

    assert result["filename"].endswith("_transcription.txt")


def test_download_error_handling(tmp_path, monkeypatch):
    monkeypatch.setattr(download_service_module, "OUTPUT_FOLDER", str(tmp_path))
    service = DownloadService()

    with pytest.raises(FileNotFoundError, match="Aucun traitement"):
        asyncio.run(service.prepare_download(uuid4(), "txt"))
