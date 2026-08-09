from pydantic import BaseModel


class HealthStatus(BaseModel):

    component: str

    status: str

    message: str


class HealthResponse(BaseModel):

    success: bool

    message: str

    checks: list[HealthStatus]
