"""Gestionnaire du modèle Faster-Whisper chargé à la demande."""

from threading import Lock
from typing import Any

from app import config


class WhisperModelManager:
    """Charge et conserve en mémoire le modèle Faster-Whisper."""

    def __init__(self, model_name: str | None = None) -> None:
        self._model: Any | None = None
        self._lock = Lock()
        self._model_name = model_name or config.WHISPER_MODEL

    def get_model(self) -> Any:
        """Retourne le modèle partagé, chargé une seule fois."""
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = self._load_model(self._model_name)

        return self._model

    @staticmethod
    def _load_model(model_name: str) -> Any:
        """Crée le modèle Faster-Whisper en CPU avec int8."""
        from faster_whisper import WhisperModel

        return WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8",
        )


whisper_manager = WhisperModelManager()
