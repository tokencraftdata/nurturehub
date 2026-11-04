import os
from dataclasses import dataclass

import jwt
from fastapi import Header, HTTPException


@dataclass(frozen=True)
class Principal:
    user_id: str


def authenticated_parent(authorization: str = Header(default="")) -> Principal:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Authentication required")
    token = authorization.removeprefix("Bearer ").strip()
    issuer = os.environ["COGNITO_ISSUER"]
    audience = os.environ["COGNITO_CLIENT_ID"]
    try:
        claims = jwt.PyJWKClient(f"{issuer}/.well-known/jwks.json").get_signing_key_from_jwt(token)
        payload = jwt.decode(token, claims.key, algorithms=["RS256"], audience=audience, issuer=issuer)
    except Exception as exc:
        raise HTTPException(401, "Invalid authentication token") from exc
    if payload.get("token_use") not in {"id", "access"} or not payload.get("sub"):
        raise HTTPException(401, "Invalid authentication claims")
    return Principal(user_id=payload["sub"])
