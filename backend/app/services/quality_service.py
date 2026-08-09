from pathlib import Path

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

            duration = await self._get_duration(
                file_path
            )

            file_size = await self._get_file_size(
                file_path
            )

            bitrate = await self._get_bitrate(
                file_path
            )

            sample_rate = await self._get_sample_rate(
                file_path
            )

            channels = await self._get_channels(
                file_path
            )

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

    async def _get_duration(
        self,
        file_path: Path
    ) -> float:

        logger.info(
            "Analyse de la durée du fichier."
        )

        raise NotImplementedError(
            "Analyse de la durée en cours de développement."
        )

    async def _get_file_size(
        self,
        file_path: Path
    ) -> int:

        logger.info(
            "Récupération de la taille du fichier."
        )

        return file_path.stat().st_size

    async def _get_bitrate(
        self,
        file_path: Path
    ) -> int:

        logger.info(
            "Analyse du débit audio."
        )

        raise NotImplementedError(
            "Analyse du débit en cours de développement."
        )

    async def _get_sample_rate(
        self,
        file_path: Path
    ) -> int:

        logger.info(
            "Analyse de la fréquence d'échantillonnage."
        )

        raise NotImplementedError(
            "Analyse de la fréquence d'échantillonnage en cours de développement."
        )

    async def _get_channels(
        self,
        file_path: Path
    ) -> int:

        logger.info(
            "Analyse du nombre de canaux."
        )

        raise NotImplementedError(
            "Analyse des canaux en cours de développement."
        )

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
