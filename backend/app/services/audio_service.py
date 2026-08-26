"""Audio extraction through FFmpeg for the transcription pipeline."""

import asyncio
import subprocess
import uuid
from pathlib import Path

from app.config import FFMPEG_PATH, OUTPUT_FOLDER
from app.utils.logger import logger


class AudioExtractionException(Exception):
    """Raised when FFmpeg cannot produce a usable WAV file."""


class FFmpegException(AudioExtractionException):
    """Raised when the configured FFmpeg executable cannot be used."""


class AudioService:
    """Extract a mono, 16 kHz PCM WAV suitable for Faster-Whisper."""

    def __init__(
        self,
        output_folder: str | Path = OUTPUT_FOLDER,
        ffmpeg_path: str = FFMPEG_PATH,
    ) -> None:
        self._output_folder = Path(output_folder)
        self._ffmpeg_path = ffmpeg_path

    async def extract_audio(self, source_path: str | Path) -> dict[str, str]:
        """Extract ``source_path`` to a uniquely named WAV file.

        The blocking FFmpeg process is run in a worker thread so this async
        service does not block the FastAPI event loop.
        """
        source = Path(source_path)
        if not source.is_file():
            raise AudioExtractionException("Source file not found")

        self._output_folder.mkdir(parents=True, exist_ok=True)
        output_path = self._output_folder / f"{source.stem}_{uuid.uuid4().hex}.wav"
        command = [
            self._ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-y",
            "-i",
            str(source),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ]

        try:
            result = await asyncio.to_thread(
                subprocess.run,
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=300,
            )
        except FileNotFoundError as exc:
            logger.error("Configured FFmpeg executable was not found")
            raise FFmpegException("FFmpeg is not available") from exc
        except subprocess.TimeoutExpired as exc:
            logger.error("FFmpeg extraction timed out for %s", source.name)
            raise AudioExtractionException("Audio extraction timed out") from exc
        except OSError as exc:
            logger.exception("Unable to start FFmpeg for %s", source.name)
            raise FFmpegException("FFmpeg could not be started") from exc

        if result.returncode != 0:
            # Keep diagnostic output in server logs only; it can include paths
            # and is not useful to an API client.
            logger.error(
                "FFmpeg failed for %s (exit code %s): %s",
                source.name,
                result.returncode,
                (result.stderr or "").strip(),
            )
            output_path.unlink(missing_ok=True)
            raise AudioExtractionException("FFmpeg could not extract the audio")

        if not output_path.is_file() or output_path.stat().st_size == 0:
            output_path.unlink(missing_ok=True)
            raise AudioExtractionException("FFmpeg did not create an audio file")

        logger.info("Audio extracted: %s -> %s", source.name, output_path.name)
        return {
            "audio_filename": output_path.name,
            "audio_path": str(output_path),
        }


audio_service = AudioService()
