import concurrent.futures
import os
import threading
import traceback
import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.schemas.cbc import CBCInput
from app.schemas.mental_health import MentalHealthInput
from app.api.mock_ehr import store_patient_cbc
from app.db.session import get_db, SessionLocal
from app.db.rls_context import apply_supabase_jwt_claims
from app.db.models import AgentSession
from app.services.agent_service import run_cbc
from app.services import case_tracking as case_svc
from app.services.mental_health_service import (
    run_mental_health_screening,
    screening_summary_for_s18,
)
from app.agents.wise_adapter import run_mental_health_wise, run_wise_agent
from app.core.config import settings
from app.core.security import get_current_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()

# Max seconds handlers wait for WISE/S18 (POST + poll). Must exceed run_poll_timeout_seconds + slack for POST/setup.
# Env WISE_TIMEOUT_SEC overrides; default = poll window + 300s buffer (full runs often 5–12+ minutes).
_pts = getattr(settings, "run_poll_timeout_seconds", 900)
_default_wise_timeout = _pts + 300
WISE_TIMEOUT_SEC = float(os.environ.get("WISE_TIMEOUT_SEC", str(max(1200, _default_wise_timeout))))


def _dedupe_recommendations(*groups: object) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for group in groups:
        if not isinstance(group, list):
            continue
        for item in group:
            text = " ".join(str(item).split()).strip()
            if not text:
                continue
            key = text.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(text)
    return out


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
    """Run CBC + WISE analysis.
    fast=true -> run WISE in single-agent fast mode.
    fast=false -> run WISE in full multi-step mode (can take longer).
    """
    patient_id = user["sub"]
    token = credentials.credentials
    poll_sec = getattr(settings, "run_poll_timeout_seconds", 900)
    req_start = time.monotonic()
    execution_mode = "fast" if fast else "full"
    print(
        f"[analyze] start patient_id={patient_id} mode={execution_mode} "
        f"poll_timeout={poll_sec}s wise_timeout={WISE_TIMEOUT_SEC}s"
    )
    apply_supabase_jwt_claims(db, patient_id)
    case_id = case_svc.create_case_and_input_message(db, patient_id, payload)
    if case_id:
        print(f"[analyze] case_id={case_id}")

    try:
        # Run CBC first (fast, local)
        cbc_result = run_cbc(payload, db, patient_id, case_id=case_id)

        # Store CBC for EHRDataMinerAgent / mockehr to fetch as labs
        store_patient_cbc(patient_id, payload.model_dump())

        # Run WISE with timeout in a thread; use a fresh DB session (thread-safe)
        wise_result = _run_wise_with_timeout(payload, patient_id, token, case_id=case_id, execution_mode=execution_mode)
        elapsed = round(time.monotonic() - req_start, 2)
        print(
            f"[analyze] complete patient_id={patient_id} mode={execution_mode} "
            f"elapsed={elapsed}s wise_flags={len(wise_result.get('flags', []) if isinstance(wise_result, dict) else [])}"
        )
        recommendations = _dedupe_recommendations(
            cbc_result.get("recommendations") if isinstance(cbc_result, dict) else None,
            wise_result.get("recommendations") if isinstance(wise_result, dict) else None,
        )
        case_svc.finalize_case_success(db, case_id, patient_id, cbc_result, wise_result, recommendations)

        # Tell clients (curl, gateways) to use at least this timeout so long S18 runs aren't aborted
        return JSONResponse(
            content={"cbc": cbc_result, "wise": wise_result, "recommendations": recommendations},
            headers={"X-Poll-Timeout-Seconds": str(poll_sec)},
        )
    except Exception as e:
        elapsed = round(time.monotonic() - req_start, 2)
        print(
            f"[analyze] error patient_id={patient_id} mode={execution_mode} "
            f"elapsed={elapsed}s error={type(e).__name__}: {e}"
        )
        case_svc.finalize_case_failure(db, case_id, patient_id, str(e))
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "traceback": tb.splitlines()[-5:] if tb else [],
            },
        )


def _run_wise_with_timeout(
    payload,
    patient_id,
    access_token: str,
    case_id: str | None = None,
    execution_mode: str = "full",
) -> dict:
    """Run WISE agent with timeout in a thread; use fresh DB session (thread-safe).

    On timeout the cancel_event is set so the background poll loop exits
    promptly instead of continuing to poll S18 and hold a DB connection.
    """
    cancel_event = threading.Event()

    def _run():
        db = SessionLocal()
        try:
            apply_supabase_jwt_claims(db, patient_id)
            return run_wise_agent(
                payload,
                patient_id,
                db,
                access_token,
                execution_mode=execution_mode,
                case_id=case_id,
                cancel_event=cancel_event,
            )
        finally:
            db.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_run)
        try:
            return future.result(timeout=WISE_TIMEOUT_SEC)
        except concurrent.futures.TimeoutError:
            cancel_event.set()
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": ["wise_timeout", "S18 did not respond within timeout"],
            }
        except Exception as e:
            cancel_event.set()
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": [f"wise_error: {str(e)[:200]}"],
            }


def _run_mh_wise_with_timeout(
    payload: MentalHealthInput,
    patient_id: str,
    access_token: str,
    local_screening: dict,
    execution_mode: str = "full",
    case_id: str | None = None,
) -> dict:
    """Run mental health S18 pass with timeout in a thread; fresh DB session per call."""
    cancel_event = threading.Event()

    def _run():
        db = SessionLocal()
        try:
            apply_supabase_jwt_claims(db, patient_id)
            return run_mental_health_wise(
                payload,
                patient_id,
                local_screening,
                db,
                access_token,
                execution_mode=execution_mode,
                case_id=case_id,
                cancel_event=cancel_event,
            )
        finally:
            db.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_run)
        try:
            return future.result(timeout=WISE_TIMEOUT_SEC)
        except concurrent.futures.TimeoutError:
            cancel_event.set()
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": ["mental_health_wise_timeout", "S18 did not respond within timeout"],
            }
        except Exception as e:
            cancel_event.set()
            return {
                "risk_level": "Unknown",
                "confidence": 0.0,
                "flags": [f"mental_health_wise_error: {str(e)[:200]}"],
            }


@router.post("/mental-health/analyze")
def mental_health_analyze(
    payload: MentalHealthInput,
    user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Local PHQ-9 / GAD-7 screening plus optional S18 narrative pass (hybrid).
    When include_s18 is false, only screening is returned (wise omitted).
    """
    patient_id = user["sub"]
    token = credentials.credentials
    poll_sec = getattr(settings, "run_poll_timeout_seconds", 900)
    req_start = time.monotonic()
    execution_mode = "fast" if payload.fast else "full"
    print(
        f"[mental-health/analyze] start patient_id={patient_id} include_s18={payload.include_s18} "
        f"mode={execution_mode} poll_timeout={poll_sec}s wise_timeout={WISE_TIMEOUT_SEC}s"
    )
    apply_supabase_jwt_claims(db, patient_id)
    case_id = case_svc.create_case_and_input_message_mental_health(db, patient_id, payload)
    if case_id:
        print(f"[mental-health/analyze] case_id={case_id}")

    try:
        screening = run_mental_health_screening(payload, db, patient_id)
        wise_result = None
        if payload.include_s18:
            summary = screening_summary_for_s18(screening)
            wise_result = _run_mh_wise_with_timeout(
                payload,
                patient_id,
                token,
                summary,
                execution_mode=execution_mode,
                case_id=case_id,
            )

        elapsed = round(time.monotonic() - req_start, 2)
        print(
            f"[mental-health/analyze] complete patient_id={patient_id} elapsed={elapsed}s "
            f"include_s18={payload.include_s18}"
        )

        body: dict = {"screening": screening}
        if wise_result is not None:
            body["wise"] = wise_result
        body["recommendations"] = _dedupe_recommendations(
            screening.get("recommendations") if isinstance(screening, dict) else None,
            wise_result.get("recommendations") if isinstance(wise_result, dict) else None,
        )

        case_svc.finalize_case_mental_health_success(
            db,
            case_id,
            patient_id,
            screening,
            wise_result,
            body["recommendations"],
        )

        return JSONResponse(
            content=body,
            headers={"X-Poll-Timeout-Seconds": str(poll_sec)},
        )
    except Exception as e:
        elapsed = round(time.monotonic() - req_start, 2)
        print(
            f"[mental-health/analyze] error patient_id={patient_id} elapsed={elapsed}s "
            f"error={type(e).__name__}: {e}"
        )
        case_svc.finalize_case_failure(db, case_id, patient_id, str(e))
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "traceback": tb.splitlines()[-5:] if tb else [],
            },
        )

