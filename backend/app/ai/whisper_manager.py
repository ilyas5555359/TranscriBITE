"""Gestionnaire du modèle Faster-Whisper chargé à la demande."""

from threading import Lock
from typing import Any

from app import config


class WhisperModelManager:
    """Charge et conserve en mémoire le modèle Faster-Whisper."""

    def __init__(self) -> None:
        self._model: Any | None = None
        self._lock = Lock()

    def get_model(self) -> Any:
        """Retourne le modèle partagé, chargé une seule fois."""
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = self._load_model()

        return self._model

    @staticmethod
    def _load_model() -> Any:
        """Crée le modèle Faster-Whisper en CPU avec int8."""
        from faster_whisper import WhisperModel

        return WhisperModel(
            config.WHISPER_MODEL,
            device="cpu",
            compute_type="int8",
        )


whisper_manager = WhisperModelManager()
