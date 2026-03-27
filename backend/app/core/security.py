from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")

JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

# Fetch JWKS once
jwks = requests.get(JWKS_URL).json()


def get_public_key(token):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header["kid"]

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

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
