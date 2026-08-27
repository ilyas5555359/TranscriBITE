from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME, APP_VERSION
from app.routers.upload import router as upload_router
from app.routers.process import router as process_router
from app.routers.progress import router as progress_router
from app.routers.download import router as download_router
from app.routers.health import router as health_router
from app.utils.logger import logger
from app.routers.transcription import router as transcription_router
from app.routers.extract import router as extract_router
from app.routers.summary import router as summary_router

logger.info("TranscriBITE backend started.")

app = FastAPI(
    title=APP_NAME,
    description="Local AI platform for audio and video transcription",
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(progress_router)
app.include_router(download_router)
app.include_router(health_router)
app.include_router(transcription_router)
app.include_router(extract_router)
app.include_router(summary_router)

@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": f"{APP_NAME} backend is running"
    }
