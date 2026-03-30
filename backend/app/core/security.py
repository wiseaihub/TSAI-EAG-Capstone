from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

security = HTTPBearer()

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

        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
