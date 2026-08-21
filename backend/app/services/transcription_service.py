"""Business service for local audio transcription."""

from pathlib import Path
from typing import Any

from app.ai.whisper_manager import WhisperModelManager, whisper_manager


class TranscriptionError(Exception):
    """Raised when audio transcription cannot be completed."""


class TranscriptionService:
    """Transcribe prepared audio files through a reusable Whisper manager."""

    def __init__(self, manager: WhisperModelManager | None = None) -> None:
        self._manager = manager or whisper_manager

    def transcribe(self, file_path: str) -> dict[str, Any]:
        """Return text, detected language, and timestamped transcript segments."""
        audio_path = Path(file_path)

        if not audio_path.is_file():
            raise FileNotFoundError("Audio file not found")

        try:
            model = self._manager.get_model()

            segments, info = model.transcribe(
                str(audio_path),
                task="transcribe",
                beam_size=5,
                vad_filter=True,
            )

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
                    segment["text"] for segment in formatted_segments
                ).strip(),
                "language": info.language,
                "segments": formatted_segments,
            }

        except TranscriptionError:
            raise

        except Exception as exc:
            raise TranscriptionError("Transcription failed") from exc


transcription_service = TranscriptionService()
