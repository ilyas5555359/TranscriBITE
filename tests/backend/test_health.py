import asyncio

from app.services import health_service as health_service_module
from app.services.health_service import HealthService


def test_health_success():
    response = asyncio.run(HealthService().check_health())

    assert response.success is True
    assert {check.component for check in response.checks} == {
        "backend",
        "configuration",
        "storage",
        "ffmpeg",
        "ai",
    }


def test_backend_check():
    check = asyncio.run(HealthService()._check_backend())

    assert check.component == "backend"
    assert check.status == "ok"


def test_configuration_check():
    check = asyncio.run(HealthService()._check_configuration())

    assert check.component == "configuration"
    assert check.status == "ok"


def test_storage_check(tmp_path, monkeypatch):
    monkeypatch.setattr(health_service_module, "UPLOAD_FOLDER", str(tmp_path / "uploads"))

    check = asyncio.run(HealthService()._check_storage())

    assert check.status == "ok"
    assert (tmp_path / "uploads").is_dir()


def test_ffmpeg_check(monkeypatch):
    monkeypatch.setattr(health_service_module.shutil, "which", lambda _: "ffmpeg")

    check = asyncio.run(HealthService()._check_ffmpeg())

    assert check.component == "ffmpeg"
    assert check.status == "ok"


def test_health_response():
    response = asyncio.run(HealthService().check_health())

    assert response.model_dump()["success"] is True
    assert len(response.model_dump()["checks"]) == 5


def test_health_error_handling(monkeypatch):
    monkeypatch.setattr(health_service_module.shutil, "which", lambda _: None)

    check = asyncio.run(HealthService()._check_ffmpeg())

    assert check.status == "error"
    assert "introuvable" in check.message


def test_ai_check_reports_unavailable_ollama(monkeypatch):
    async def unavailable_ollama():
        return False

    monkeypatch.setattr(
        health_service_module.summary_service,
        "check_availability",
        unavailable_ollama,
    )

    check = asyncio.run(HealthService()._check_ai_dependencies())

    assert check.component == "ai"
    assert check.status == "error"
    assert "Ollama" in check.message
