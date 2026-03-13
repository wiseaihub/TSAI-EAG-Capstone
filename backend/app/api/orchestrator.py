import concurrent.futures
import os
import traceback

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.schemas.cbc import CBCInput
from app.api.mock_ehr import store_patient_cbc
from app.db.session import get_db, SessionLocal
from app.db.models import AgentSession
from app.services.agent_service import run_cbc
from app.agents.wise_adapter import run_wise_agent
from app.core.config import settings
from app.core.security import get_current_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()

# Max seconds /analyze will wait for WISE (S18 run + poll). Must exceed run_poll_timeout_seconds.
# Env WISE_TIMEOUT_SEC overrides; else poll_timeout + 120s so ~70s S18 runs don't hit handler timeout.
_default_wise_timeout = getattr(settings, "run_poll_timeout_seconds", 300) + 120
WISE_TIMEOUT_SEC = float(os.environ.get("WISE_TIMEOUT_SEC", str(max(920, _default_wise_timeout))))


@router.get("/agent-sessions")
def list_agent_sessions(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
):
    """Return recent agent_sessions for the current user (verify DB persistence)."""
    patient_id = user["sub"]
    rows = (
        db.query(AgentSession)
        .filter(AgentSession.patient_id == patient_id)
        .order_by(desc(AgentSession.timestamp))
        .limit(limit)
        .all()
    )
    return [
        {
            "session_id": r.session_id,
            "agent_name": r.agent_name,
            "risk_level": r.risk_level,
            "confidence": r.confidence,
            "flags": r.flags,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None,
        }
        for r in rows
    ]


@router.post("/analyze")
def analyze(
    payload: CBCInput,
    user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    fast: bool = False,
):
    """Run CBC + WISE analysis. Use ?fast=true to skip WISE and return CBC only (instant).
    When fast=false, S18 may take 1–3 min; clients should use a timeout >= GET /health poll_timeout_seconds (e.g. 300s).
    """
    patient_id = user["sub"]
    token = credentials.credentials
    poll_sec = getattr(settings, "run_poll_timeout_seconds", 300)

    try:
        # Run CBC first (fast, local)
        cbc_result = run_cbc(payload, db, patient_id)

        # Store CBC for EHRDataMinerAgent / mockehr to fetch as labs
        store_patient_cbc(patient_id, payload.model_dump())

        if fast:
            return {"cbc": cbc_result, "wise": None}

        # Run WISE with timeout in a thread; use a fresh DB session (thread-safe)
        wise_result = _run_wise_with_timeout(payload, patient_id, token)

        # Tell clients (curl, gateways) to use at least this timeout so long S18 runs aren't aborted
        return JSONResponse(
            content={"cbc": cbc_result, "wise": wise_result},
            headers={"X-Poll-Timeout-Seconds": str(poll_sec)},
        )
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "traceback": tb.splitlines()[-5:] if tb else [],
            },
        )


def _run_wise_with_timeout(payload, patient_id, access_token: str) -> dict:
    """Run WISE agent with timeout in a thread; use fresh DB session (thread-safe)."""
    def _run():
        db = SessionLocal()
        try:
            return run_wise_agent(payload, patient_id, db, access_token)
        finally:
            db.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_run)
        try:
            return future.result(timeout=WISE_TIMEOUT_SEC)
        except concurrent.futures.TimeoutError:
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": ["wise_timeout", "S18 did not respond within timeout"],
            }
        except Exception as e:
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": [f"wise_error: {str(e)[:200]}"],
            }

