from app.core.celery_app import celery_app
from app.schemas.cbc import CBCInput
from app.db.session import SessionLocal
from app.services.agent_service import run_cbc


@celery_app.task(bind=True)
def run_cbc_task(self, payload: dict, patient_id: str):
    """Run CBC analysis in worker; payload = CBCInput.model_dump()."""
    db = SessionLocal()
    try:
        cbc_input = CBCInput(**payload)
        result = run_cbc(cbc_input, db, patient_id)
        return result
    finally:
        db.close()
