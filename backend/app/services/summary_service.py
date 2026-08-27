"""Service de résumé via Ollama (modèle gemma2:2b)."""

import httpx

from app.utils.logger import logger


OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma2:2b"


class SummaryError(Exception):
    """Erreur lors de la génération du résumé."""


class SummaryService:
    """Génère un résumé du texte transcrit via Ollama."""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
    ) -> None:
        self._base_url = base_url
        self._model = model

    async def generate_summary(
        self,
        text: str,
        language: str = "fr",
    ) -> dict[str, str]:
        """Envoie le texte à Ollama et retourne le résumé."""

        if not text or not text.strip():
            raise ValueError("Le texte à résumer est vide.")

        prompt = self._build_prompt(text, language)

        try:
            async with httpx.AsyncClient(
                timeout=120.0,
            ) as client:

                response = await client.post(
                    f"{self._base_url}/api/generate",
                    json={
                        "model": self._model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"num_predict": 48},
                    },
                )

                response.raise_for_status()

                result = response.json()

                summary_text = result.get("response", "").strip()

                if not summary_text:
                    raise SummaryError(
                        "Ollama a retourné un résumé vide."
                    )

                logger.info("Résumé généré avec succès.")

                return {
                    "summary": summary_text,
                    "model": self._model,
                }

        except httpx.ConnectError as error:
            logger.error("Impossible de se connecter à Ollama: %s", error)
            raise SummaryError(
                "Ollama n'est pas accessible. Vérifiez qu'il est démarré."
            ) from error

        except httpx.HTTPStatusError as error:
            logger.error("Erreur HTTP Ollama: %s", error)
            raise SummaryError(
                "Erreur lors de la communication avec Ollama."
            ) from error

        except Exception as error:
            logger.error("Erreur lors de la génération du résumé: %s", error)
            raise SummaryError(
                "Échec de la génération du résumé."
            ) from error

    @staticmethod
    def _build_prompt(text: str, language: str) -> str:
        """Construit le prompt pour Ollama."""

        if language == "fr":
            return (
                "Tu es un assistant spécialisé dans le résumé de texte. "
                "Résume le texte suivant comme une étiquette en 1 à 2 "
                "lignes maximum et 20 mots maximum, en français. Utilise "
                "une phrase courte, sans introduction ni répétition.\n\n"
                f"Texte à résumer :\n{text}\n\n"
                "Résumé :"
            )

        return (
            "You are a text summarization assistant. "
            "Summarize the following text like a label in 1 to 2 lines and "
            "20 words maximum. Use one short sentence without an "
            "introduction or repetition.\n\n"
            f"Text to summarize:\n{text}\n\n"
            "Summary:"
        )

    async def check_availability(self) -> bool:
        """Vérifie si Ollama est accessible."""

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self._base_url}/api/tags")
                return response.status_code == 200

        except Exception:
            return False


summary_service = SummaryService()
