from dotenv import load_dotenv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def _resolve_storage_path(variable_name: str) -> str:
    """Resolve a storage path from the .env relative to the backend directory."""
    configured_path = os.getenv(variable_name)
    if not configured_path:
        raise RuntimeError(f"Missing required configuration: {variable_name}")

    path = Path(configured_path).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return str(path.resolve())


APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

UPLOAD_FOLDER = _resolve_storage_path("UPLOAD_FOLDER")
OUTPUT_FOLDER = _resolve_storage_path("OUTPUT_FOLDER")
TEMP_FOLDER = _resolve_storage_path("TEMP_FOLDER")
CACHE_FOLDER = _resolve_storage_path("CACHE_FOLDER")
LOG_FOLDER = _resolve_storage_path("LOG_FOLDER")

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE")

FFMPEG_PATH = os.getenv("FFMPEG_PATH")

WHISPER_MODEL = os.getenv("WHISPER_MODEL")
