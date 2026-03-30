"""Dual-write helpers for cases / messages / audit (orchestrator + /cbc/analyze)."""

import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models import AgentMessage, AuditEvent, Case
from app.schemas.cbc import CBCInput
from app.schemas.mental_health import MentalHealthInput


def create_case_and_input_message(db: Session, patient_id: str, payload: CBCInput) -> str | None:
    """Create a case row and capture the incoming request as a user message."""
    case_id = str(uuid4())
    payload_dict = payload.model_dump()
    try:
        db.add(
            Case(
                id=case_id,
                user_id=patient_id,
                status="running",
                title="CBC analysis request",
                input_payload=payload_dict,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        db.flush()
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="user",
                content=json.dumps(payload_dict, default=str),
                meta={"source": "orchestrator:/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_created",
                event_payload={"source": "/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
        return case_id
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during case creation: {type(e).__name__}: {e}")
        return None


def create_case_and_input_message_cbc(db: Session, patient_id: str, payload: CBCInput) -> str | None:
    """Same as create_case_and_input_message but tags source as /cbc/analyze."""
    case_id = str(uuid4())
    payload_dict = payload.model_dump()
    try:
        db.add(
            Case(
                id=case_id,
                user_id=patient_id,
                status="running",
                title="CBC analysis request (cbc route)",
                input_payload=payload_dict,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        db.flush()
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="user",
                content=json.dumps(payload_dict, default=str),
                meta={"source": "cbc:/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_created",
                event_payload={"source": "/cbc/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
        return case_id
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during case creation: {type(e).__name__}: {e}")
        return None


def create_case_and_input_message_mental_health(
    db: Session, patient_id: str, payload: MentalHealthInput
) -> str | None:
    """Create case + user message for POST /mental-health/analyze."""
    case_id = str(uuid4())
    payload_dict = payload.model_dump()
    try:
        db.add(
            Case(
                id=case_id,
                user_id=patient_id,
                status="running",
                title="Mental health screening",
                input_payload=payload_dict,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        db.flush()
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="user",
                content=json.dumps(payload_dict, default=str),
                meta={"source": "orchestrator:/mental-health/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_created",
                event_payload={"source": "/mental-health/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
        return case_id
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during MH case creation: {type(e).__name__}: {e}")
        return None


def finalize_case_mental_health_success(
    db: Session,
    case_id: str | None,
    patient_id: str,
    screening: dict,
    wise_result: dict | None,
    recommendations: list[str],
) -> None:
    if not case_id:
        return
    try:
        row = db.query(Case).filter(Case.id == case_id).first()
        if row:
            row.status = "completed"
            row.updated_at = datetime.utcnow()
        body: dict = {"screening": screening, "recommendations": recommendations}
        if wise_result is not None:
            body["wise"] = wise_result
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="assistant",
                content=json.dumps(body, default=str),
                meta={"source": "orchestrator:/mental-health/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_completed",
                event_payload={
                    "recommendation_count": len(recommendations),
                    "route": "mental-health/analyze",
                    "include_s18": wise_result is not None,
                },
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during MH success finalize: {type(e).__name__}: {e}")


def finalize_case_success(
    db: Session,
    case_id: str | None,
    patient_id: str,
    cbc_result: dict,
    wise_result: dict,
    recommendations: list[str],
) -> None:
    if not case_id:
        return
    try:
        row = db.query(Case).filter(Case.id == case_id).first()
        if row:
            row.status = "completed"
            row.updated_at = datetime.utcnow()
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="assistant",
                content=json.dumps(
                    {"cbc": cbc_result, "wise": wise_result, "recommendations": recommendations},
                    default=str,
                ),
                meta={"source": "orchestrator:/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_completed",
                event_payload={"recommendation_count": len(recommendations)},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during success finalize: {type(e).__name__}: {e}")


def finalize_case_cbc_only(
    db: Session,
    case_id: str | None,
    patient_id: str,
    cbc_result: dict,
    recommendations: list[str],
) -> None:
    """Complete case after /cbc/analyze (no WISE block)."""
    if not case_id:
        return
    try:
        row = db.query(Case).filter(Case.id == case_id).first()
        if row:
            row.status = "completed"
            row.updated_at = datetime.utcnow()
        db.add(
            AgentMessage(
                case_id=case_id,
                run_id=None,
                role="assistant",
                content=json.dumps(
                    {"cbc": cbc_result, "recommendations": recommendations},
                    default=str,
                ),
                meta={"source": "cbc:/analyze"},
                created_at=datetime.utcnow(),
            )
        )
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_completed",
                event_payload={"recommendation_count": len(recommendations), "route": "cbc"},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during cbc finalize: {type(e).__name__}: {e}")


def finalize_case_failure(db: Session, case_id: str | None, patient_id: str, error_text: str) -> None:
    if not case_id:
        return
    try:
        row = db.query(Case).filter(Case.id == case_id).first()
        if row:
            row.status = "failed"
            row.updated_at = datetime.utcnow()
        db.add(
            AuditEvent(
                user_id=patient_id,
                entity_type="case",
                entity_id=case_id,
                event_type="case_failed",
                event_payload={"error": error_text[:500]},
                created_at=datetime.utcnow(),
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[case_tracking] dual-write skipped during failure finalize: {type(e).__name__}: {e}")
