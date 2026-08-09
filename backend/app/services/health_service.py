from app.schemas.health_schema import (
    HealthResponse,
    HealthStatus
)

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

        return HealthResponse(

            success=True,

            message="Vérification du système terminée.",

            checks=checks
        )

    async def _check_backend(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification du backend."
        )

        raise NotImplementedError(
            "Vérification du backend en cours de développement."
        )

    async def _check_configuration(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification de la configuration."
        )

        raise NotImplementedError(
            "Vérification de la configuration en cours de développement."
        )

    async def _check_storage(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification du stockage."
        )

        raise NotImplementedError(
            "Vérification du stockage en cours de développement."
        )

    async def _check_ffmpeg(
        self
    ) -> HealthStatus:

        logger.info(
            "Vérification de FFmpeg."
        )

        raise NotImplementedError(
            "Vérification de FFmpeg en cours de développement."
        )
