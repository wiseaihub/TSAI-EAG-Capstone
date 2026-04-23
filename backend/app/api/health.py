from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "WISE AI Backend",
        "poll_timeout_seconds": settings.run_poll_timeout_seconds,
        "tenancy_tier": settings.tenancy_tier,
        "data_region": settings.tenancy_default_region,
    }
