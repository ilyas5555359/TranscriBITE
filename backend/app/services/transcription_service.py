"""Service de transcription audio locale avec Faster-Whisper."""

from pathlib import Path
from typing import Any

from app.ai.whisper_manager import WhisperModelManager, whisper_manager


class TranscriptionError(Exception):
    """Erreur lors de la transcription audio."""


class TranscriptionService:
    """Transcrit les fichiers audio préparés avec Faster-Whisper."""

    def __init__(
        self,
        manager: WhisperModelManager | None = None,
    ) -> None:
        self._manager = manager or whisper_manager

    def transcribe(
        self,
        file_path: str,
        language: str = "auto",
    ) -> dict[str, Any]:
        """Retourne le texte, la langue et les segments horodatés."""

        audio_path = Path(file_path)

        if not audio_path.is_file():
            raise FileNotFoundError(
                "Audio file not found"
            )

        try:
            model = self._manager.get_model()

            options = {
                "task": "transcribe",
                "beam_size": 5,
                "vad_filter": True,
            }
            if language != "auto":
                options["language"] = language

            segments, info = model.transcribe(str(audio_path), **options)

            formatted_segments = [
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
                for segment in segments
            ]

            return {
                "text": " ".join(
                    segment["text"]
                    for segment in formatted_segments
                ).strip(),
                "language": info.language,
                "segments": formatted_segments,
            }

        except Exception as error:
            raise TranscriptionError(
                "Transcription failed"
            ) from error


transcription_service = TranscriptionService()
