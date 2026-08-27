"""Service d'analyse de qualité audio via FFprobe."""

import asyncio
import json
import subprocess
from pathlib import Path

from app.config import FFMPEG_PATH
from app.services.file_service import check_file_exists
from app.utils.logger import logger


class QualityService:

    async def analyze_audio(
        self,
        file_path: Path
    ) -> dict:

        logger.info(
            "Analyse de la qualité audio."
        )

        try:

            check_file_exists(file_path)

            probe_data = await self._run_ffprobe(file_path)

            duration = self._extract_duration(probe_data)

            file_size = await self._get_file_size(file_path)

            bitrate = self._extract_bitrate(probe_data)

            sample_rate = self._extract_sample_rate(probe_data)

            channels = self._extract_channels(probe_data)

            return await self._build_quality_report(
                duration=duration,
                file_size=file_size,
                bitrate=bitrate,
                sample_rate=sample_rate,
                channels=channels
            )

        except Exception as error:

            await self._handle_error(error)

            raise

    async def _run_ffprobe(
        self,
        file_path: Path
    ) -> dict:
        """Exécute FFprobe et retourne les métadonnées JSON."""

        ffprobe_path = FFMPEG_PATH.replace("ffmpeg", "ffprobe")

        command = [
            ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]

        try:
            result = await asyncio.to_thread(
                subprocess.run,
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except FileNotFoundError as exc:
            logger.error("FFprobe introuvable.")
            raise RuntimeError(
                "FFprobe n'est pas disponible."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            logger.error("FFprobe timeout pour %s", file_path.name)
            raise RuntimeError(
                "Analyse audio interrompue (timeout)."
            ) from exc

        if result.returncode != 0:
            logger.error(
                "FFprobe a échoué pour %s: %s",
                file_path.name,
                (result.stderr or "").strip()
            )
            raise RuntimeError(
                "FFprobe n'a pas pu analyser le fichier."
            )

        return json.loads(result.stdout)

    @staticmethod
    def _extract_duration(probe_data: dict) -> float:
        """Extrait la durée depuis les données FFprobe."""

        format_data = probe_data.get("format", {})
        duration_str = format_data.get("duration")

        if duration_str:
            return round(float(duration_str), 2)

        for stream in probe_data.get("streams", []):
            if stream.get("codec_type") == "audio":
                dur = stream.get("duration")
                if dur:
                    return round(float(dur), 2)

        return 0.0

    @staticmethod
    def _extract_bitrate(probe_data: dict) -> int:
        """Extrait le débit en bits/s depuis les données FFprobe."""

        format_data = probe_data.get("format", {})
        bit_rate = format_data.get("bit_rate")

        if bit_rate:
            return int(bit_rate)

        for stream in probe_data.get("streams", []):
            if stream.get("codec_type") == "audio":
                br = stream.get("bit_rate")
                if br:
                    return int(br)

        return 0

    @staticmethod
    def _extract_sample_rate(probe_data: dict) -> int:
        """Extrait la fréquence d'échantillonnage."""

        for stream in probe_data.get("streams", []):
            if stream.get("codec_type") == "audio":
                sr = stream.get("sample_rate")
                if sr:
                    return int(sr)

        return 0

    @staticmethod
    def _extract_channels(probe_data: dict) -> int:
        """Extrait le nombre de canaux audio."""

        for stream in probe_data.get("streams", []):
            if stream.get("codec_type") == "audio":
                ch = stream.get("channels")
                if ch:
                    return int(ch)

        return 0

    async def _get_file_size(
        self,
        file_path: Path
    ) -> int:

        logger.info(
            "Récupération de la taille du fichier."
        )

        return file_path.stat().st_size

    async def _build_quality_report(

        self,

        duration: float,

        file_size: int,

        bitrate: int,

        sample_rate: int,

        channels: int

    ) -> dict:

        logger.info(
            "Construction du rapport qualité."
        )

        return {

            "duration": duration,

            "file_size": file_size,

            "bitrate": bitrate,

            "sample_rate": sample_rate,

            "channels": channels
        }

    async def _handle_error(
        self,
        error: Exception
    ) -> None:

        logger.error(
            str(error)
        )


quality_service = QualityService()
