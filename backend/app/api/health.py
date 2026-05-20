import os

import requests
from fastapi import APIRouter

from app.agents.wise_adapter import _get_s18_base_url
from app.core.config import settings

router = APIRouter()


def _probe_s18_health() -> dict:
    base = _get_s18_base_url()
    if not base:
        return {"reachable": False, "error": "S18_BASE_URL is empty"}
    url = f"{base}/health"
    try:
        resp = requests.get(url, timeout=8)
        return {
            "reachable": resp.ok,
            "status_code": resp.status_code,
            "url": url,
            "body_preview": (resp.text or "")[:200] if resp.ok else (resp.text or "")[:200],
        }
    except requests.RequestException as exc:
        return {"reachable": False, "url": url, "error": str(exc)}


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "WISE AI Backend",
        "poll_timeout_seconds": settings.run_poll_timeout_seconds,
        "tenancy_tier": settings.tenancy_tier,
        "data_region": settings.tenancy_default_region,
        "s18_base_url": _get_s18_base_url(),
        "s18_probe": _probe_s18_health(),
        "supabase_url_configured": bool(os.environ.get("SUPABASE_URL")),
    }
