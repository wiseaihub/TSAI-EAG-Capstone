import os

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


def _railway_deploy_info() -> dict | None:
    """Railway sets these when the deployment was triggered from GitHub (not always on manual redeploy)."""
    mapping = (
        ("RAILWAY_GIT_COMMIT_SHA", "git_sha"),
        ("RAILWAY_GIT_BRANCH", "git_branch"),
        ("RAILWAY_GIT_COMMIT_MESSAGE", "git_commit_message"),
    )
    out: dict = {}
    for env_key, json_key in mapping:
        val = os.getenv(env_key)
        if val:
            out[json_key] = val
    return out or None


@router.get("/health", tags=["Health"])
def health_check():
    payload = {
        "status": "ok",
        "service": "WISE AI Backend",
        "poll_timeout_seconds": settings.run_poll_timeout_seconds,
        "tenancy_tier": settings.tenancy_tier,
        "data_region": settings.tenancy_default_region,
    }
    deploy = _railway_deploy_info()
    if deploy:
        payload["deploy"] = deploy
    return payload
