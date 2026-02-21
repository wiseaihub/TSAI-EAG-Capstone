from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.cbc import CBCInput
from app.db.session import get_db
from app.services.agent_service import run_cbc
from app.agents.fusion_engine import fuse_results
from app.core.security import get_current_user

router = APIRouter()

@router.post("/analyze")
def analyze(
    payload: CBCInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    patient_id = user["sub"]

    results = {}
    results["cbc"] = run_cbc(payload, db, patient_id)

    return results

