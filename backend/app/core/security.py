import os
import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.db.models import UserProfile
from app.db.session import get_db

security = HTTPBearer()
APP_ROLES = {"doctor", "patient"}

_jwks_cache: dict | None = None


def _get_jwks() -> dict:
    """Load JWKS lazily so imports do not require network (CI, unit tests)."""
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache
    base = os.getenv("SUPABASE_URL")
    if not base:
        raise HTTPException(status_code=500, detail="SUPABASE_URL not configured")
    url = f"{base.rstrip('/')}/auth/v1/.well-known/jwks.json"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    _jwks_cache = resp.json()
    return _jwks_cache


def get_public_key(token):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header["kid"]

    jwks = _get_jwks()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key

    raise HTTPException(status_code=401, detail="Public key not found")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        key = get_public_key(token)

        payload = jwt.decode(
            token,
            key,
            algorithms=["ES256"],
            audience="authenticated",
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing subject")
        app_role = _resolve_or_create_user_role(db, str(user_id))
        payload["app_role"] = app_role
        return payload

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def _resolve_or_create_user_role(db: Session, user_id: str) -> str:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile is None:
        try:
            profile = UserProfile(user_id=user_id, role="patient")
            db.add(profile)
            db.commit()
            return "patient"
        except Exception:
            # Handle concurrent first-login upserts by retrying a lookup.
            db.rollback()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile is None:
                raise
    role = str(profile.role or "").strip().lower()
    if role not in APP_ROLES:
        raise HTTPException(status_code=403, detail="User role is not provisioned")
    return role


def require_doctor(user=Depends(get_current_user)):
    if user.get("app_role") != "doctor":
        raise HTTPException(status_code=403, detail="Doctor access required")
    return user


def require_patient_or_doctor(user=Depends(get_current_user)):
    if user.get("app_role") not in APP_ROLES:
        raise HTTPException(status_code=403, detail="Provisioned role required")
    return user
