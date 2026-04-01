from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.cbc import CBCInput
from app.db.session import get_db
from app.db.rls_context import apply_supabase_jwt_claims
from app.services.agent_service import run_cbc
from app.services import case_tracking as case_svc
from app.core.security import require_doctor

router = APIRouter()


@router.post("/analyze")
def analyze_cbc(
    payload: CBCInput,
    user=Depends(require_doctor),
    db: Session = Depends(get_db),
):
    """CBC-only analysis; dual-writes runtime tables same as POST /analyze (without WISE)."""
    patient_id = user["sub"]
    apply_supabase_jwt_claims(db, patient_id)
    case_id = case_svc.create_case_and_input_message_cbc(db, patient_id, payload)
    try:
        result = run_cbc(payload, db, patient_id, case_id=case_id)
        recs = result.get("recommendations") if isinstance(result, dict) else []
        case_svc.finalize_case_cbc_only(db, case_id, patient_id, result, recs or [])
        return result
    except Exception as e:
        case_svc.finalize_case_failure(db, case_id, patient_id, str(e))
        raise
