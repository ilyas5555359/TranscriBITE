from fastapi import APIRouter

from app.schemas.health_schema import HealthResponse
from app.services.health_service import HealthService


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


health_service = HealthService()


@router.get(
    "",
    response_model=HealthResponse
)
async def check_health():

    return await health_service.check_health()
