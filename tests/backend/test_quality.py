import asyncio
from pathlib import Path

import pytest

from app.services.quality_service import QualityService


PROBE_DATA = {
    "format": {"duration": "2.5", "bit_rate": "128000"},
    "streams": [{"codec_type": "audio", "sample_rate": "16000", "channels": 1}],
}


def test_analyze_audio(tmp_path, monkeypatch):
    source = tmp_path / "sample.wav"
    source.write_bytes(b"audio")
    service = QualityService()

    async def fake_probe(_):
        return PROBE_DATA

    monkeypatch.setattr(service, "_run_ffprobe", fake_probe)
    result = asyncio.run(service.analyze_audio(source))

    assert result == {
        "duration": 2.5,
        "file_size": 5,
        "bitrate": 128000,
        "sample_rate": 16000,
        "channels": 1,
    }


def test_get_duration():
    assert QualityService._extract_duration(PROBE_DATA) == 2.5


def test_get_file_size(tmp_path):
    source = tmp_path / "sample.wav"
    source.write_bytes(b"12345")

    assert asyncio.run(QualityService()._get_file_size(source)) == 5


def test_get_bitrate():
    assert QualityService._extract_bitrate(PROBE_DATA) == 128000


def test_get_sample_rate():
    assert QualityService._extract_sample_rate(PROBE_DATA) == 16000


def test_get_channels():
    assert QualityService._extract_channels(PROBE_DATA) == 1


def test_build_quality_report():
    report = asyncio.run(QualityService()._build_quality_report(1.0, 2, 3, 4, 5))

    assert report == {
        "duration": 1.0,
        "file_size": 2,
        "bitrate": 3,
        "sample_rate": 4,
        "channels": 5,
    }


def test_quality_error_handling(tmp_path):
    with pytest.raises(FileNotFoundError, match="File not found"):
        asyncio.run(QualityService().analyze_audio(Path(tmp_path / "missing.wav")))
