"""Focused tests for FFmpeg audio extraction."""

import asyncio
import importlib
import shutil
import subprocess
import wave
from pathlib import Path

import pytest
from fastapi import FastAPI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

import sys

sys.path.insert(0, str(BACKEND_ROOT))

from app.services.audio_service import AudioExtractionException, AudioService
from app.routers.extract import router as extract_router

audio_service_module = importlib.import_module("app.services.audio_service")


def _write_wav(path: Path, *, sample_rate: int = 16_000, channels: int = 1) -> None:
    """Create a small valid PCM WAV fixture without requiring FFmpeg."""
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"\x00\x00" * (sample_rate * channels // 10))


def test_extract_audio_rejects_missing_source(tmp_path: Path) -> None:
    service = AudioService(output_folder=tmp_path / "outputs", ffmpeg_path="ffmpeg")

    with pytest.raises(AudioExtractionException, match="Source file not found"):
        asyncio.run(service.extract_audio(tmp_path / "missing.mp3"))


def test_extract_router_can_be_loaded() -> None:
    app = FastAPI()
    app.include_router(extract_router)

    assert any(route.path == "/extract" for route in extract_router.routes)


def test_extract_audio_creates_whisper_compatible_wav(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.mp3"
    source.write_bytes(b"fixture")
    service = AudioService(output_folder=tmp_path / "outputs", ffmpeg_path="ffmpeg-test")
    called_command: list[str] = []

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        called_command.extend(command)
        _write_wav(Path(command[-1]))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(audio_service_module.subprocess, "run", fake_run)

    result = asyncio.run(service.extract_audio(source))
    output = Path(result["audio_path"])

    assert output.is_file()
    assert result["audio_filename"].endswith(".wav")
    assert called_command[:1] == ["ffmpeg-test"]
    assert "-ac" in called_command and called_command[called_command.index("-ac") + 1] == "1"
    assert "-ar" in called_command and called_command[called_command.index("-ar") + 1] == "16000"
    assert "-c:a" in called_command and called_command[called_command.index("-c:a") + 1] == "pcm_s16le"
    with wave.open(str(output), "rb") as wav_file:
        assert wav_file.getnchannels() == 1
        assert wav_file.getframerate() == 16_000
        assert wav_file.getsampwidth() == 2


def test_extract_audio_hides_ffmpeg_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"fixture")
    service = AudioService(output_folder=tmp_path / "outputs", ffmpeg_path="ffmpeg-test")

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 1, "", "private FFmpeg diagnostic")

    monkeypatch.setattr(audio_service_module.subprocess, "run", fake_run)

    with pytest.raises(AudioExtractionException, match="FFmpeg could not extract the audio") as error:
        asyncio.run(service.extract_audio(source))

    assert "private FFmpeg diagnostic" not in str(error.value)


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg is not available in PATH")
def test_extract_audio_with_real_ffmpeg(tmp_path: Path) -> None:
    """Integration test using a real audio fixture when FFmpeg is installed."""
    source = tmp_path / "source.wav"
    _write_wav(source, sample_rate=8_000, channels=2)
    service = AudioService(
        output_folder=tmp_path / "outputs",
        ffmpeg_path=shutil.which("ffmpeg") or "ffmpeg",
    )

    result = asyncio.run(service.extract_audio(source))

    with wave.open(result["audio_path"], "rb") as wav_file:
        assert wav_file.getnchannels() == 1
        assert wav_file.getframerate() == 16_000
        assert wav_file.getsampwidth() == 2
