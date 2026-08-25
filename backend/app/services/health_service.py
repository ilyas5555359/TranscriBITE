from pathlib import Path
import shutil

from app.schemas.health_schema import (
    HealthResponse,
    HealthStatus
)

from app.config import UPLOAD_FOLDER
from app.utils.logger import logger


class HealthService:

    async def check_health(
        self
    ) -> HealthResponse:

        logger.info(
            "Vérification de l'état du backend."
        )

        checks = [
            await self._check_backend(),
            await self._check_configuration(),
            await self._check_storage(),
            await self._check_ffmpeg()
        ]

        success = all(
            check.status == "ok"
            for check in checks
        )

        return HealthResponse(
            success=success,
            message="Vérification du système terminée.",
            checks=checks
        )

    async def _check_backend(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification du backend."
        )

        return HealthStatus(
            component="backend",
            status="ok",
            message="Backend opérationnel."
        )

    async def _check_configuration(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification de la configuration."
        )

        try:
            if not UPLOAD_FOLDER:
                raise ValueError(
                    "UPLOAD_FOLDER non configuré."
                )

            return HealthStatus(
                component="configuration",
                status="ok",
                message="Configuration valide."
            )

        except Exception as error:
            return HealthStatus(
                component="configuration",
                status="error",
                message=str(error)
            )

    async def _check_storage(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification du stockage."
        )

        try:
            storage_path = Path(UPLOAD_FOLDER)
            storage_path.mkdir(
                parents=True,
                exist_ok=True
            )

            if not storage_path.is_dir():
                raise OSError(
                    "Le dossier de stockage est inaccessible."
                )

            return HealthStatus(
                component="storage",
                status="ok",
                message="Stockage accessible."
            )

        except Exception as error:
            return HealthStatus(
                component="storage",
                status="error",
                message=str(error)
            )

    async def _check_ffmpeg(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification de FFmpeg."
        )

        try:
            ffmpeg_path = shutil.which("ffmpeg")

            if not ffmpeg_path:
                raise FileNotFoundError(
                    "FFmpeg introuvable dans le PATH."
                )

            return HealthStatus(
                component="ffmpeg",
                status="ok",
                message="FFmpeg disponible."
            )

        except Exception as error:
            return HealthStatus(
                component="ffmpeg",
                status="error",
                message=str(error)
            )
        