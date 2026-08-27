from pathlib import Path

import pytest

from app.services.transcription_service import TranscriptionError, TranscriptionService


class FakeSegment:
    start = 0.0
    end = 1.25
    text = " Bonjour "


class FakeInfo:
    language = "fr"


class FakeModel:
    def transcribe(self, *_args, **_kwargs):
        return iter([FakeSegment()]), FakeInfo()


class FakeManager:
    def get_model(self):
        return FakeModel()


def test_transcribe_formats_text_language_and_timestamps(tmp_path):
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"audio")

    result = TranscriptionService(FakeManager()).transcribe(str(audio_path))

    assert result == {
        "text": "Bonjour",
        "language": "fr",
        "segments": [{"start": 0.0, "end": 1.25, "text": "Bonjour"}],
    }


def test_transcribe_passes_selected_language(tmp_path):
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"audio")

    result = TranscriptionService(FakeManager()).transcribe(
        str(audio_path),
        language="fr",
    )

    assert result["language"] == "fr"


def test_transcribe_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        TranscriptionService(FakeManager()).transcribe(str(tmp_path / "missing.wav"))


def test_transcribe_wraps_model_errors(tmp_path):
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"audio")

    class BrokenManager:
        def get_model(self):
            raise RuntimeError("model unavailable")

    with pytest.raises(TranscriptionError):
        TranscriptionService(BrokenManager()).transcribe(str(audio_path))
