from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION
from app.routers.upload import router as upload_router
from app.routers.process import router as process_router
from app.routers.progress import router as progress_router
from app.routers.download import router as download_router
from app.routers.health import router as health_router

from app.utils.logger import logger


logger.info("TranscriBITE backend started.")

app = FastAPI(
    title=APP_NAME,
    description="Local AI platform for audio and video transcription",
    version=APP_VERSION
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(progress_router)
app.include_router(download_router)
app.include_router(health_router)

@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": f"{APP_NAME} backend is running"
    }
