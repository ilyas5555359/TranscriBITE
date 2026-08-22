from dotenv import load_dotenv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
TEMP_FOLDER = os.getenv("TEMP_FOLDER")
CACHE_FOLDER = os.getenv("CACHE_FOLDER")
LOG_FOLDER = os.getenv("LOG_FOLDER")

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE")

FFMPEG_PATH = os.getenv("FFMPEG_PATH")

WHISPER_MODEL = os.getenv("WHISPER_MODEL")