"""Service de téléchargement : génère les fichiers TXT et JSON."""

import json
from datetime import datetime
from pathlib import Path
from uuid import UUID

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from app.config import OUTPUT_FOLDER, WHISPER_MODEL
from app.models.processing_state import processing_state
from app.utils.logger import logger


class DownloadService:

    @staticmethod
    def _format_duration(seconds: float | int | None) -> str:
        if seconds is None:
            return "Non disponible"
        total_seconds = float(seconds)
        minutes, remaining_seconds = divmod(int(total_seconds), 60)
        return f"{minutes} min {remaining_seconds:02d} s"

    @staticmethod
    def _format_datetime(value: datetime | None) -> str:
        return value.strftime("%d/%m/%Y %H:%M:%S") if value else "Non disponible"

    def __init__(self):
        self._output_folder = Path(OUTPUT_FOLDER)

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

        if download_format == "pdf":
            return await self._prepare_pdf_download(file_id=file_id)

        raise ValueError(
            "Format de téléchargement non supporté."
        )

    async def _validate_download(
        self,
        file_id: UUID,
        download_format: str
    ) -> None:

        if download_format not in ["txt", "json", "pdf"]:

            raise ValueError(
                "Format de téléchargement non supporté."
            )

        logger.info(
            f"Validation du téléchargement du fichier {file_id}"
        )

    async def _get_processing_data(
        self,
        file_id: UUID
    ):
        """Récupère l'état et les résultats stockés du traitement."""

        proc = await processing_state.get_processing(file_id)
        if proc is None:
            raise FileNotFoundError(
                f"Aucun traitement trouvé pour {file_id}"
            )

        return proc

    async def _prepare_txt_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement TXT pour {file_id}"
        )

        self._output_folder.mkdir(parents=True, exist_ok=True)

        processing = await self._get_processing_data(file_id)
        transcription = getattr(processing, "transcription_result", None)
        summary = getattr(processing, "summary_result", None)

        text_content = ""
        if transcription:
            text_content = transcription.get("text", "")
        if summary and summary.get("summary"):
            text_content = f"{text_content}\n\nRésumé :\n{summary['summary']}"

        filename = f"{file_id.hex}_transcription.txt"
        output_path = self._output_folder / filename

        output_path.write_text(text_content, encoding="utf-8")

        logger.info(f"Fichier TXT créé : {output_path}")

        return {
            "file_id": file_id,
            "filename": filename,
            "download_format": "txt",
            "file_path": str(output_path),
        }

    async def _prepare_json_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement JSON pour {file_id}"
        )

        self._output_folder.mkdir(parents=True, exist_ok=True)

        processing = await self._get_processing_data(file_id)
        transcription = getattr(processing, "transcription_result", None)
        summary = getattr(processing, "summary_result", None)

        json_content = {
            "file_id": str(file_id),
            "transcription": transcription or {},
            "summary": summary or {},
        }

        filename = f"{file_id.hex}_transcription.json"
        output_path = self._output_folder / filename

        output_path.write_text(
            json.dumps(json_content, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        logger.info(f"Fichier JSON créé : {output_path}")

        return {
            "file_id": file_id,
            "filename": filename,
            "download_format": "json",
            "file_path": str(output_path),
        }

    async def _prepare_pdf_download(
        self,
        file_id: UUID
    ) -> dict:

        logger.info(
            f"Préparation du téléchargement PDF pour {file_id}"
        )

        processing = await self._get_processing_data(file_id)
        transcription = getattr(processing, "transcription_result", None) or {}
        quality = getattr(processing, "quality_result", None) or {}
        summary = getattr(processing, "summary_result", None) or {}
        original_filename = processing.original_filename or ""
        suffix = Path(original_filename).suffix.lower()
        media_type = "Vidéo" if suffix in {".mp4", ".avi", ".mov", ".mkv"} else (
            "Audio" if suffix in {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
            else "Non disponible"
        )
        execution_seconds = None
        if processing.started_at and processing.finished_at:
            execution_seconds = (
                processing.finished_at - processing.started_at
            ).total_seconds()
        filename = f"{file_id.hex}_transcription.pdf"
        output_path = self._output_folder / filename
        self._output_folder.mkdir(parents=True, exist_ok=True)

        document = canvas.Canvas(
            str(output_path),
            pagesize=A4,
            pageCompression=0,
        )
        document.setTitle(f"Rapport de transcription {file_id}")
        page_width, page_height = A4
        left = 50
        right = page_width - 50
        y = page_height - 55

        def write_line(value: str = "", font="Helvetica", size=10):
            nonlocal y
            if y < 55:
                document.showPage()
                y = page_height - 55
            document.setFont(font, size)
            safe_value = str(value).encode("latin-1", "replace").decode("latin-1")
            document.drawString(left, y, safe_value)
            y -= size + 5

        def write_wrapped(value: str, font="Helvetica", size=10):
            words = str(value or "").split()
            line = ""
            for word in words:
                candidate = f"{line} {word}".strip()
                if stringWidth(candidate, font, size) > right - left and line:
                    write_line(line, font, size)
                    line = word
                else:
                    line = candidate
            if line:
                write_line(line, font, size)

        def section(title: str):
            write_line()
            write_line(title, "Helvetica-Bold", 12)

        section("RAPPORT DE TRANSCRIPTION - TranscriBITE")
        write_line(f"Nom du fichier : {original_filename or 'Non disponible'}")
        write_line(f"Type : {media_type}")
        write_line(f"Durée du média : {self._format_duration(quality.get('duration'))}")
        write_line(f"Date du traitement : {self._format_datetime(processing.started_at)}")

        section("1. Informations de transcription")
        write_line(f"Langue : {transcription.get('language', 'Non disponible')}")
        write_line(f"Modèle : {WHISPER_MODEL}")
        write_line(f"Statut : {processing.current_status.value}")
        write_line(f"Fin du traitement : {self._format_datetime(processing.finished_at)}")
        write_line(
            f"Temps d'exécution : {self._format_duration(execution_seconds)}"
        )

        section("2. Résumé")
        write_wrapped(summary.get("summary", "Aucun résumé disponible."))
        write_line(f"Modèle de résumé : {summary.get('model', 'Non disponible')}")

        section("3. Informations techniques")
        for label, key in (("Taille", "file_size"), ("Débit", "bitrate"),
                           ("Fréquence d'échantillonnage", "sample_rate"),
                           ("Canaux", "channels")):
            write_line(f"{label} : {quality.get(key, 'Non disponible')}")
        segments = transcription.get("segments", [])
        write_line(f"Nombre de segments : {len(segments)}")

        section("4. Transcription complète")
        write_wrapped(transcription.get("text", "Aucune transcription disponible."))

        section("5. Timestamps")
        for segment in segments:
            write_wrapped(
                f"[{segment.get('start', '?')} - {segment.get('end', '?')}] "
                f"{segment.get('text', '')}"
            )

        section("6. Informations TranscriBITE")
        write_line("Traitement réalisé localement.")
        write_line("Aucun service cloud utilisé.")
        document.save()

        return {
            "file_id": file_id,
            "filename": filename,
            "download_format": "pdf",
            "file_path": str(output_path),
        }
