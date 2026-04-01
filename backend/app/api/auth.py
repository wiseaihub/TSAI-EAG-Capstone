from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user
from app.db.models import UserProfile
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def auth_me(user=Depends(get_current_user)):
    return {
        "sub": user.get("sub"),
        "email": user.get("email"),
        "app_role": user.get("app_role"),
    }


class DoctorProvisionInput(BaseModel):
    user_id: str


@router.post("/provision-doctor")
def provision_doctor(
    payload: DoctorProvisionInput,
    db: Session = Depends(get_db),
    x_provision_secret: str | None = Header(default=None, alias="X-Provision-Secret"),
):
    expected = settings.doctor_provision_secret
    if not expected:
        raise HTTPException(status_code=503, detail="Doctor provisioning is not configured")
    if x_provision_secret != expected:
        raise HTTPException(status_code=403, detail="Invalid provisioning secret")

    user_id = str(payload.user_id or "").strip()
    if not user_id:
        raise HTTPException(status_code=422, detail="user_id is required")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile is None:
        profile = UserProfile(user_id=user_id, role="doctor")
        db.add(profile)
        status = "created"
    else:
        profile.role = "doctor"
        status = "updated"
    db.commit()
    return {"user_id": user_id, "app_role": "doctor", "status": status}
