from fastapi import APIRouter, Depends

from app.schemas.cbc import CBCInput
from app.core.security import get_current_user
from app.core.celery_app import celery_app
from app.tasks.cbc_tasks import run_cbc_task
from celery.result import AsyncResult

router = APIRouter()


@router.post("/analyze")
def analyze_cbc(
    payload: CBCInput,
    user=Depends(get_current_user),
):
    """Enqueue CBC analysis; returns task_id. Poll GET /cbc/task/{task_id} for result."""
    patient_id = user["sub"]
    task = run_cbc_task.delay(payload.model_dump(), patient_id)
    return {"task_id": task.id}


@router.get("/task/{task_id}")
def get_task_status(task_id: str):
    """Return task status and result (PENDING | SUCCESS | FAILURE)."""
    result = AsyncResult(task_id, app=celery_app)
    state = result.state
    resp = {"task_id": task_id, "status": state}
    if state == "SUCCESS":
        resp["result"] = result.result
    elif state == "FAILURE":
        resp["result"] = str(result.result) if result.result else None
    else:
        resp["result"] = None
    return resp
