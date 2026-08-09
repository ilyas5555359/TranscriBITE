from uuid import UUID

from app.utils.logger import logger


class DownloadService:

    def __init__(self):

        pass


    async def prepare_download(
        self,
        file_id: UUID,
        download_format: str
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement pour le fichier {file_id}"
        )

        await self._validate_download(
            file_id=file_id,
            download_format=download_format
        )

        if download_format == "txt":

            return await self._prepare_txt_download(
                file_id=file_id
            )

        if download_format == "json":

            return await self._prepare_json_download(
                file_id=file_id
            )

        raise ValueError(
            "Format de téléchargement non supporté."
        )


    async def _validate_download(
        self,
        file_id: UUID,
        download_format: str
    ) -> None:

        if download_format not in [
            "txt",
            "json"
        ]:

            raise ValueError(
                "Format de téléchargement non supporté."
            )

        logger.info(
            f"Validation du téléchargement du fichier {file_id}"
        )

        #
        # Vérifications futures :
        #
        # vérifier que le fichier existe
        # vérifier que le traitement est terminé
        # vérifier que les résultats existent
        #


    async def _prepare_txt_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement TXT pour {file_id}"
        )

        #
        # Futures étapes :
        #
        # récupérer la transcription
        # créer le fichier TXT
        # enregistrer le fichier
        #

        return {

            "file_id": file_id,

            "filename": "transcription.txt",

            "download_format": "txt"
        }


    async def _prepare_json_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement JSON pour {file_id}"
        )

        #
        # Futures étapes :
        #
        # récupérer la transcription
        # récupérer le résumé
        # créer le fichier JSON
        # enregistrer le fichier
        #

        return {

            "file_id": file_id,

            "filename": "transcription.json",

            "download_format": "json"
        }


    async def _prepare_pdf_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement PDF pour {file_id}"
        )

        raise NotImplementedError(
            "Le téléchargement PDF sera développé dans une future version."
        )
