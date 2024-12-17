from fastapi import HTTPException
from utils.auth import decode_access_token


def is_admin(token: str) -> bool:
    decoded = decode_access_token(token)
    role = decoded["role"]
    if role != "admin":
        raise HTTPException(status_code=403, detail="only Admin can access this endpoint")
    return True


def is_regular_user(token: str) -> bool:
    decoded = decode_access_token(token)
    role = decoded["role"]
    if role != "regular":
        raise HTTPException(status_code=403, detail="only Regulsr User can access this endpoint")
    return True
